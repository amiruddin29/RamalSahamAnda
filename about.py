import streamlit as st
from streamlit_player import st_player
from streamlit_pdf_viewer import pdf_viewer

# Custom button component
def st_button(label, url, description, icon_size):
    st.markdown(
        f"""
        <a href="{url}" target="_blank" style="text-decoration: none;">
            <button style="background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: {icon_size}px;">
                {label}
            </button>
        </a>
        <p>{description}</p>
        """,
        unsafe_allow_html=True
    )

def app():
    st.title('E-learning for Beginners')
    st.subheader('Introduction')
    st.write("""
    Welcome to the beginner's guide on stock market analysis. This e-learning platform provides a series of curated video tutorials to help you understand key concepts and financial statements used in the stock market.
    """)

    tabs = st.tabs(["Basic", "Overview", "Financial", "Fundamental", "Technical", "Graph & Indicator", "E-book"])

    with tabs[0]:
        st.subheader("Information on opening a brokerage account")
        st_player('https://youtu.be/APczKuabhMw?si=74EC-tvFA3BZboT7')
        st.markdown("---")
        st.subheader("Overview of different types of brokerage accounts")
        st_player('https://youtu.be/_MKv1B5VrXc?si=D9O6gsCXR2JooDMk')
        st.markdown("---")
        st.subheader("Guides on how to place buy and sell orders")
        st_player('https://youtu.be/Ev07sFwFxq4?si=VRtY2NPpXI-hJydf')
        st.markdown("---")
        st.subheader("Tips for beginners on making their first investment")
        st_player('https://youtu.be/xLAxEYhXJSY?si=6FS7CVdm9fb-Bb18')

    with tabs[1]:
        st.subheader('Stock Market Overview')
        st.write("13-minute explanation about stock market")
        st_player('https://youtu.be/T37YvxMTofc?si=b5ydCRgyNGHQP03i')

    with tabs[2]:
        st.subheader('Analyzing Financial Statements')
        st.markdown("---")
        st.subheader("How to analyze a balance sheet")
        st_player('https://youtu.be/7THNE8xEcHk?si=daCGI5AqOkIFTrjJ')
        st.markdown("---")
        st.subheader("How to analyze an income statement")
        st_player('https://youtu.be/uVHGgSXtQmE?si=eBQHXewNZjpwJJW0')
        st.markdown("---")
        st.subheader("Cash Flow Statement for beginners")
        st_player('https://youtu.be/DiVPAjgmnj0?si=VV8IAc4FNMe-jt-K')

    with tabs[3]:
        st.subheader('Fundamental Analysis')
        st_player('https://youtu.be/3BOE1A8HXeE?si=DCdXV87QEr5o2QFL')

    with tabs[4]:
        st.subheader('Technical Analysis')
        st.markdown("---")
        st.subheader("Moving Averages (MA) Part 1")
        st_player('https://youtu.be/4R2CDbw4g88?si=-NpzlmHXfGNK6qhH')
        st.markdown("---")
        st.subheader("Moving Averages (MA) Part 2")
        st_player('https://youtu.be/5rMkQurfxrE?si=xo1WHDuOBhGCkO20')

    with tabs[5]:
        st.subheader('Reading Graphs and Indicators')
        st.markdown("---")
        st.subheader("Beginner guide to read graphs")
        st_player('https://youtu.be/eynxyoKgpng?si=jPPl70sLN88wYR1w')
        st.markdown("---")
        st.subheader("Beginner guide to read Return on Stock")
        st_player('https://youtu.be/6hlh-TJgmXk?si=09yTaJQiZKUqgn20')

    with tabs[6]:
        st.subheader("E-book")
        # URL of the PDF file
        #pdf_url = "https://industri.fatek.unpatti.ac.id/wp-content/uploads/2019/03/McGraw.Hill_.Understanding-Stocks.pdf"
        pdf_url = "./stocksinfo.pdf"
        pdf_display = f'<iframe src="{pdf_url}" width="1000" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

if __name__ == "__main__":
    app()
