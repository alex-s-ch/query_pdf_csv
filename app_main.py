##
import streamlit as st
from pdf_tool import pdf_tool
from csv_tool import csv_tool


def main():
    st.set_page_config(page_title="File Analysis Tool", page_icon=":books:")

    if "show_pdf_tool" not in st.session_state:
        st.session_state.show_pdf_tool = True
    if "show_csv_tool" not in st.session_state:
        st.session_state.show_csv_tool = False

    col1, col2 = st.columns(2)
    if col1.button("PDF Analysis"):
        st.session_state.show_pdf_tool = True
        st.session_state.show_csv_tool = False

    if col2.button("CSV Analysis"):
        st.session_state.show_csv_tool = True
        st.session_state.show_pdf_tool = False

    if st.session_state.show_pdf_tool:
        pdf_tool()

    if st.session_state.show_csv_tool:
        csv_tool()


if __name__ == '__main__':
    main()
