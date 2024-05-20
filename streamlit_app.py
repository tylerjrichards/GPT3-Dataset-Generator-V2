# ----------------------Importing libraries----------------------

import streamlit as st
from streamlit_pills import pills
import pandas as pd
import openai

# Imports for AgGrid
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# ----------------------Importing utils.py----------------------

# For Snowflake (from Tony's utils.py)
import io
from utils import (
    connect_to_snowflake,
    load_data_to_snowflake,
    load_data_to_postgres,
    connect_to_postgres,
)

# ----------------------Page config--------------------------------------

st.set_page_config(page_title="GPT3 Dataset Generator", page_icon="🤖")

# ----------------------Sidebar section--------------------------------

# st.image(
#    "Gifs/header.gif",
# )

st.image("Gifs/boat_new.gif")

c30, c31, c32 = st.columns([0.2, 0.1, 3])

with c30:

    st.caption("")

    st.image("openai.png", width=60)

with c32:

    st.title("GPT3 Dataset Generator")

st.write(
    "This app generates datasets using GPT3. It was created for the ❄️ Snowflake Snowvation Hackathon"
)

tabMain, tabInfo, tabTo_dos = st.tabs(["Main", "Info", "To-do's"])

with tabInfo:
    st.write("")
    st.write("")

    st.subheader("🤖 What is GPT-3?")
    st.markdown(
        "[GPT-3](https://en.wikipedia.org/wiki/GPT-3) is a large language generation model developed by [OpenAI](https://openai.com/) that can generate human-like text. It has a capacity of 175 billion parameters and is trained on a vast dataset of internet text. It can be used for tasks such as language translation, chatbot language generation, and content generation etc."
    )

    st.subheader("🎈 What is Streamlit?")
    st.markdown(
        "[Streamlit](https://streamlit.io) is an open-source Python library that allows users to create interactive, web-based data visualization and machine learning applications without the need for extensive web development knowledge"
    )

    st.write("---")

    st.subheader("📖 Resources")
    st.markdown(
        """
    - OpenAI
        - [OpenAI Playground](https://beta.openai.com/playground)
        - [OpenAI Documentation](https://beta.openai.com/docs)    
    - Streamlit
        - [Documentation](https://docs.streamlit.io/)
        - [Gallery](https://streamlit.io/gallery)
        - [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
        - [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
        - Deploy your apps using [Streamlit Community Cloud](https://streamlit.io/cloud) in just a few clicks 
    """
    )

with tabTo_dos:

    with st.expander("To-do", expanded=True):
        st.write(
            """
        - [p2] Currently, the results are displayed even if the submit button isn't pressed.
        - [p2] There is still an issue with the index where the first element from the JSON is not being displayed.
        - [Post Hackathon] To limit the number of API calls and costs, let's cap the maximum number - of results to 5. Alternatively, we can consider removing the free API key.

        """
        )
        st.write("")

    with st.expander("Done", expanded=True):
        st.write(
            """
        - [p2] Check if the Json file is working
        - [p2] On Github, remove any unused images and GIFs.
        - [p1] Add that for postgress - localhost is required
        - [p2] Rename the CSV and JSON as per the st-pills variable
        - [p2] Change the color of the small arrow
        - [p1] Adjust the size of the Gifs
        - Add a streamlit badge in the `ReadMe` file
        - Add the message "Please enter your API key or choose the `Free Key` option."
        - Include a `ReadMe` file
        - Add a section for the Snowflake credentials
        - Remove password from the Python file
        - Add screenshots to the `ReadMe` file
        - Include forms in the snowflake postgres section
        - Remove the hashed code in the Python file
        - Include additional information in the 'info' tab
        - p1] Fix the download issue by sorting it via session state
        - [p1] Make the dataframe from this app editable
        - Add more gifs to the app
        - Change the color scheme to Snowflake Blue
        - Include a section for Snowflake credentials
        - Change the colors of the arrows, using this tool (https://lottiefiles.com/lottie-to-gif/convert)
        - Try new prompts and implement the best ones
        - Add a config file for the color scheme
        - Include an option menu using this tool (https://github.com/victoryhb/streamlit-option-menu)
        - Display a message when the API key is not provided
        - Fix the arrow and rearrange the layout for the API key message
        - Check and improve the quality of the prompt output
        - Send the app to Tony and upload it to GitHub
        - Re-arrange the data on the sidebar
        - Change the colors of both gifs to match the overall color scheme
        - Add context about the app being part of the snowvation project
        - Add a button to convert the data to JSON format
        - Include the Snowflake logo
        - Add a submit button to block API calls unless pressed
        - Add a tab with additional information
        - Resize the columns in the st.form section
        - Add the ability to add the dataset to Snowflake
        - Create a section with pills, showcasing examples
        - Change the main emoji
        - Change the emoji in the tab (page_icon)
        - [INFO] Sort out the issue with credits



        """
        )
        st.write("")

    with st.expander("Not needed", expanded=True):
        st.write(
            """
            - Check index issue in readcsv (not an issue as I've changed the script)
            - Add the mouse gif (doesn't fit)
            - Ask Lukas - automatically resize the columns of a DataFrame
        """
        )
        st.write("")

    st.write("")
    st.write("")
    st.write("")


with tabMain:

    key_choice = st.sidebar.radio(
        "",
        (
            "Your Key",
            "Free Key (capped)",
        ),
        horizontal=True,
    )

    if key_choice == "Your Key":

        API_Key = st.sidebar.text_input(
            "First, enter your OpenAI API key", type="password"
        )

    elif key_choice == "Free Key (capped)":

        API_Key = st.secrets["API_KEY"]

    image_arrow = st.sidebar.image(
        "Gifs/blue_grey_arrow.gif",
    )

    if key_choice == "Free Key (capped)":

        image_arrow.empty()

    else:

        st.write("")

        st.sidebar.caption(
            "No OpenAI API key? Get yours [here!](https://openai.com/blog/api-no-waitlist/)"
        )
        pass

    st.write("")

    c30, c31, c32 = st.columns([0.2, 0.1, 3])

    st.subheader("① Build your dataset")

    example = pills(
        "",
        [
            "Sci-fi Movies",
            "Animals",
            "Pop Songs",
            "POTUS's Twitter",
            "Blank",
        ],
        [
            "🍿",
            "🐎",
            "🎵",
            "🇺🇸",
            "👻",
        ],
        label_visibility="collapsed",
    )

    if "counter" not in st.session_state:
        st.session_state.counter = 0

    def increment():
        st.session_state.counter += 1

    if example == "Sci-fi Movies":

        with st.form("my_form"):

            text_input = st.text_input(
                "What is the topic of your dataset?", value="Sci-fi movies"
            )

            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                column_01 = st.text_input("1st column", value="Title")

            with col2:
                column_02 = st.text_input("2nd column", value="Year")

            with col3:
                column_03 = st.text_input("3rd column", value="PG rating")

            col1, col2 = st.columns(2, gap="medium")

            with col1:
                number = st.number_input(
                    "How many rows do you want?",
                    value=5,
                    min_value=1,
                    max_value=20,
                    step=5,
                    help="The maximum number of rows is 20.",
                )

            with col2:
                engine = st.radio(
                    "GPT3 engine",
                    (
                        "Davinci",
                        ## Depricated ## "Curie",
                        "Babbage",
                        "Turbo"
                    ),
                    horizontal=True,
                    help="Davinci is the most powerful engine, but it's also the slowest. Curie is the fastest, but it's also the least powerful. Babbage is somewhere in the middle.",
                )

                if engine == "Davinci":
                    engine = "davinci-002"
                ## Depricated ##elif engine == "Curie":
                ## Depricated ##    engine = "curie-instruct-beta-v2"
                elif engine == "Babbage":
                    engine = "babbage-002"
                elif engine == "Turbo":
                    engine = "gpt-3.5-turbo-instruct"

            st.write("")

            submitted = st.form_submit_button("Build my dataset! ✨", on_click=increment)

    elif example == "Animals":

        with st.form("my_form"):

            text_input = st.text_input(
                "What is the topic of your dataset?", value="Fastest animals on earth"
            )

            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                column_01 = st.text_input("1st column", value="Animal")

            with col2:
                column_02 = st.text_input("2nd column", value="Speed")

            with col3:
                column_03 = st.text_input("3rd column", value="Weight")

            col1, col2 = st.columns(2, gap="medium")

            with col1:
                number = st.number_input(
                    "How many rows do you want?",
                    value=5,
                    min_value=1,
                    max_value=20,
                    step=5,
                    help="The maximum number of rows is 50.",
                )

            with col2:
                engine = st.radio(
                    "GPT3 engine",
                    (
                        "Davinci",
                        ## Depricated ## "Curie",
                        "Babbage",
                        "Turbo"
                    ),
                    horizontal=True,
                    help="Davinci is the most powerful engine, but it's also the slowest. Curie is the fastest, but it's also the least powerful. Babbage is somewhere in the middle.",
                )

                if engine == "Davinci":
                    engine = "davinci-002"
                ## Depricated ##elif engine == "Curie":
                ## Depricated ##    engine = "curie-instruct-beta-v2"
                elif engine == "Babbage":
                    engine = "babbage-002"
                elif engine == "Turbo":
                    engine = "gpt-3.5-turbo-instruct"

            st.write("")

            submitted = st.form_submit_button("Build my dataset! ✨", on_click=increment)

    elif example == "Stocks":

        with st.form("my_form"):

            text_input = st.text_input(
                "What is the topic of your dataset?", value="Stocks"
            )

            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                column_01 = st.text_input("1st column", value="Ticker")

            with col2:
                column_02 = st.text_input("2nd column", value="Price")

            with col3:
                column_03 = st.text_input("3rd column", value="Exchange")

            col1, col2 = st.columns(2, gap="medium")

            with col1:
                number = st.number_input(
                    "How many rows do you want?",
                    value=5,
                    min_value=1,
                    max_value=20,
                    step=5,
                    help="The maximum number of rows is 50.",
                )

            with col2:
                engine = st.radio(
                    "GPT3 engine",
                    (
                        "Davinci",
                        ## Depricated ## "Curie",
                        "Babbage",
                        "Turbo"
                    ),
                    horizontal=True,
                    help="Davinci is the most powerful engine, but it's also the slowest. Curie is the fastest, but it's also the least powerful. Babbage is somewhere in the middle.",
                )

                if engine == "Davinci":
                    engine = "davinci-002"
                ## Depricated ##elif engine == "Curie":
                ## Depricated ##    engine = "curie-instruct-beta-v2"
                elif engine == "Babbage":
                    engine = "babbage-002"
                elif engine == "Turbo":
                    engine = "gpt-3.5-turbo-instruct"
                    
            st.write("")

            submitted = st.form_submit_button("Build my dataset! ✨", on_click=increment)

    elif example == "POTUS's Twitter":

        with st.form("my_form"):

            text_input = st.text_input(
                "What is the topic of your dataset?", value="POTUS's Twitter accounts"
            )

            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                column_01 = st.text_input("1st column", value="Name")

            with col2:
                column_02 = st.text_input("2nd column", value="Twitter handle")

            with col3:
                column_03 = st.text_input("3rd column", value="# of followers")

            col1, col2 = st.columns(2, gap="medium")

            with col1:
                number = st.number_input(
                    "How many rows do you want?",
                    value=5,
                    min_value=1,
                    max_value=20,
                    step=5,
                    help="The maximum number of rows is 50.",
                )

            with col2:
                engine = st.radio(
                    "GPT3 engine",
                    (
                        "Davinci",
                        ## Depricated ## "Curie",
                        "Babbage",
                        "Turbo"
                    ),
                    horizontal=True,
                    help="Davinci is the most powerful engine, but it's also the slowest. Curie is the fastest, but it's also the least powerful. Babbage is somewhere in the middle.",
                )

                if engine == "Davinci":
                    engine = "davinci-002"
                ## Depricated ##elif engine == "Curie":
                ## Depricated ##    engine = "curie-instruct-beta-v2"
                elif engine == "Babbage":
                    engine = "babbage-002"
                elif engine == "Turbo":
                    engine = "gpt-3.5-turbo-instruct"

            st.write("")

            submitted = st.form_submit_button("Build my dataset! ✨")

    elif example == "Pop Songs":

        with st.form("my_form"):

            text_input = st.text_input(
                "What is the topic of your dataset?",
                value="Most famous songs of all time",
            )

            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                column_01 = st.text_input("1st column", value="Song")

            with col2:
                column_02 = st.text_input("2nd column", value="Artist")

            with col3:
                column_03 = st.text_input("3rd column", value="Genre")

            col1, col2 = st.columns(2, gap="medium")

            with col1:
                number = st.number_input(
                    "How many rows do you want?",
                    value=5,
                    min_value=1,
                    max_value=20,
                    step=5,
                    help="The maximum number of rows is 50.",
                )

            with col2:
                engine = st.radio(
                    "GPT3 engine",
                    (
                        "Davinci",
                        ## Depricated ## "Curie",
                        "Babbage",
                        "Turbo"
                    ),
                    horizontal=True,
                    help="Davinci is the most powerful engine, but it's also the slowest. Curie is the fastest, but it's also the least powerful. Babbage is somewhere in the middle.",
                )

                if engine == "Davinci":
                    engine = "davinci-002"
                ## Depricated ##elif engine == "Curie":
                ## Depricated ##    engine = "curie-instruct-beta-v2"
                elif engine == "Babbage":
                    engine = "babbage-002"
                elif engine == "Turbo":
                    engine = "gpt-3.5-turbo-instruct"

            st.write("")

            submitted = st.form_submit_button("Build my dataset! ✨")

    elif example == "Blank":

        with st.form("my_form"):

            text_input = st.text_input("What is the topic of your dataset?", value="")

            col1, col2, col3 = st.columns(3, gap="small")

            with col1:
                column_01 = st.text_input("1st column", value="")

            with col2:
                column_02 = st.text_input("2nd column", value="")

            with col3:
                column_03 = st.text_input("3rd column", value="")

            col1, col2 = st.columns(2, gap="medium")

            with col1:
                number = st.number_input(
                    "How many rows do you want?",
                    value=5,
                    min_value=1,
                    max_value=20,
                    step=5,
                    help="The maximum number of rows is 50.",
                )

            with col2:
                engine = st.radio(
                    "GPT3 engine",
                    (
                        "Davinci",
                        ## Depricated ## "Curie",
                        "Babbage",
                        "Turbo"
                    ),
                    horizontal=True,
                    help="Davinci is the most powerful engine, but it's also the slowest. Curie is the fastest, but it's also the least powerful. Babbage is somewhere in the middle.",
                )

                if engine == "Davinci":
                    engine = "davinci-002"
                ## Depricated ##elif engine == "Curie":
                ## Depricated ##    engine = "curie-instruct-beta-v2"
                elif engine == "Babbage":
                    engine = "babbage-002"
                elif engine == "Turbo":
                    engine = "gpt-3.5-turbo-instruct"

            st.write("")

            submitted = st.form_submit_button("Build my dataset! ✨")

    # ----------------------API key section----------------------------------

    number = number + 1

    if not API_Key and not submitted:

        st.stop()

    if not API_Key and submitted:

        st.info("Please enter your API key or choose the `Free Key` option.")
        st.stop()

    if st.session_state.counter >= 100:

        pass

    # ----------------------API key section----------------------------------

    if not submitted and st.session_state.counter == 0:

        c30, c31, c32 = st.columns([1, 0.01, 4])

        with c30:

            st.image("Gifs/arrow_small_new.gif")
            st.caption("")

        with c32:

            st.caption("")
            st.caption("")

            st.info(
                "Enter your dataset's criteria and click the button to generate it."
            )

            st.stop()

    elif st.session_state.counter > 0:

        c30, c31, c32 = st.columns([1, 0.9, 3])

        openai.api_key = API_Key

        # ----------------------API call section----------------------------------

        ## Depricated ## response = openai.Completion.create(
        response = openai.completions.create(
            model=engine,
            prompt=f"Please provide a list of the top {number} {text_input} along with the following information in a three-column spreadsheet: {column_01}, {column_02}, and {column_03}. The columns should be labeled as follows: {column_01} | {column_02} | {column_03}",
            temperature=0.5,
            max_tokens=1707,
            top_p=1,
            best_of=2,
            frequency_penalty=0,
            presence_penalty=0,
        )

        st.write("___")

        st.subheader("② Check the results")

        with st.expander("See the API Json output"):
            response
        
        ## output_code = response["choices"][0]["text"]
        output_code = response.choices[0].text

        # ----------------------Dataframe section----------------------------------

        # create pandas DataFrame from string
        df = pd.read_csv(io.StringIO(output_code), sep="|")
        # get the number of columns in the dataframe
        num_columns = len(df.columns)

        # create a list of column names
        column_names = ["Column {}".format(i) for i in range(1, num_columns + 1)]

        # add the header to the dataframe
        df.columns = column_names

        # specify the mapping of old column names to new column names
        column_mapping = {
            "Column 1": column_01,
            "Column 2": column_02,
            "Column 3": column_03,
        }

        # rename the columns of the dataframe
        df = df.rename(columns=column_mapping)

        st.write("")

        # ----------------------AgGrid section----------------------------------

        gd = GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(editable=True, groupable=True)
        gd.configure_selection(selection_mode="multiple")
        gridoptions = gd.build()
        grid_table = AgGrid(
            df,
            gridOptions=gridoptions,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme="material",
        )

        # df

        # ----------------------Download section--------------------------------------

        c30, c31, c32, c33 = st.columns([1, 0.01, 1, 2.5])

        with c30:

            @st.cache
            def convert_df(df):
                return df.to_csv().encode("utf-8")

            csv = convert_df(df)

            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{example} dataset .csv",
                mime="text/csv",
            )

        with c32:

            json_string = df.to_json(orient="records")

            st.download_button(
                label="Download JSON",
                data=json_string,
                file_name="data_set_sample.json",
                mime="text/csv",
            )

    st.write("___")

    st.subheader("③ Load data to Databases")

    # Data to load to database(s)
    # df = pd.read_csv("philox-testset-1.csv")

    # Get user input for data storage option
    storage_option = st.radio(
        "Select data storage option:",
        (
            "Snowflake",
            "PostgreSQL",
        ),
        horizontal=True,
    )

    # Get user input for data storage option
    # Snowflake = st.selectbox(
    #    "Select data storage option:", ["Snowflake", "Snowflake"]
    # )

    @st.cache(allow_output_mutation=True)
    def reset_form_fields():
        user = ""
        password = ""
        account = ""
        warehouse = ""
        database = ""
        schema = ""
        table = ""
        host = ""
        port = ""

    if storage_option == "Snowflake":
        st.subheader("`Enter Snowflake Credentials`👇")
        # Get user input for Snowflake credentials

        with st.form("my_form_db"):

            col1, col2 = st.columns(2, gap="small")

            with col1:
                user = st.text_input("Username:", value="TONY")
            with col2:
                password = st.text_input("Password:", type="password")

            with col1:
                account = st.text_input("Account:", value="jn27194.us-east4.gcp")
            with col2:
                warehouse = st.text_input("Warehouse:", value="NAH")

            with col1:
                database = st.text_input("Database:", value="SNOWVATION")
            with col2:
                schema = st.text_input("Schema:", value="PUBLIC")

            table = st.text_input("Table:")

            st.write("")

            submitted = st.form_submit_button("Load to Snowflake")

        # Load the data to Snowflake
        if submitted:
            # if st.button("Load data to Snowflake"):
            if (
                user
                and password
                and account
                and warehouse
                and database
                and schema
                and table
            ):
                conn = connect_to_snowflake(
                    username=user,
                    password=password,
                    account=account,
                    warehouse=warehouse,
                    database=database,
                    schema=schema,
                )
                if conn:
                    load_data_to_snowflake(df, conn, table)
            else:
                st.warning("Please enter all Snowflake credentials")

    elif storage_option == "PostgreSQL":
        st.subheader("`Enter PostgreSQL Credentials`👇")
        st.error("Localhost only")
        # Get user input for PostgreSQL credentials

        with st.form("my_form_db"):

            col1, col2 = st.columns(2, gap="small")

            with col1:
                user = st.text_input("Username:", value="postgres")
            with col2:
                password = st.text_input("Password:", type="password")
            with col1:
                host = st.selectbox("Host:", ["localhost", "other"])
                if host == "other":
                    host = st.text_input("Enter host:")
            with col2:
                port = st.text_input("Port:", value="5432")
            with col1:
                database = st.text_input("Database:", value="snowvation")
            with col2:
                table = st.text_input("Table:")

            st.write("")

            submitted = st.form_submit_button("Load to PostgreSQL")

        # Load the data to PostgreSQL
        # if st.button("Load data to PostgreSQL"):
        if submitted:
            if user and password and host and port and database and table:
                conn = connect_to_postgres(
                    username=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database,
                )
                if conn:
                    load_data_to_postgres(df, conn, table)
            else:
                st.warning("Please enter all PostgreSQL credentials and table name")

    # Reset form fields when storage_option changes
    reset_form_fields()
