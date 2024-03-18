
import streamlit as st
import datetime
import pandas as pd
import time

st.set_page_config(layout='wide')

# style yellow if values between -350 and -450 like (351, 401),
# style red if value less than -450 like(-451, -500) else white
def style_dataframe(df):
    return df.style.applymap(
        lambda x: 'background-color: yellow' if ((x < -350) & (x > -450)) else ('background-color: red; color: white' if x <= -450 else 'background-color: white'),
        subset=['Senti_2003', 'Senti_2051', 'Senti_6760', 'Senti_9771']
    )

def time_difference_in_minutes(dt1, dt2):
    timedelta = dt2 - dt1
    return (timedelta.total_seconds() // 60)

try:
    if st.session_state["my_input"] == 'VIKABH':
        st.title('DC PS SENTI')
        logout = st.button('Logout')

        if logout:
            st.markdown('<span style="color: blue;">Please go to login in the side menu</span>', unsafe_allow_html=True)
            st.session_state["my_input"] = None
            # st.experimental_rerun()
            exit(0)

        # Create placeholders for dynamic content
        time_display = st.empty()
        time_delay_alert = st.empty()
        # summary_placeholder = st.empty()
        complete_placeholder = st.empty()

        while True:
            try:
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Fetch data
                # summary_df = pd.read_csv('D:\\Hemish\\DV2.csv')
                complete_df = pd.read_csv('senti_ps.csv')
                time_frame = complete_df['DT'].iloc[0]
                del complete_df['DT']

                time_frame = pd.to_datetime(time_frame)
                current_time_dt = pd.to_datetime(current_time)
                time_diff_min = time_difference_in_minutes(current_time_dt, time_frame)
                time_diff_min = abs(time_diff_min)

                # Update time_display placeholder
                time_display.write(f'CT {current_time}   |   DC PS SENTI time {time_frame}', format='md')

                # if time_diff_min > 3:
                #     time_delay_alert.markdown('<span style="color: red">Data delay greater than 2 minutes!</span>',
                #                               unsafe_allow_html=True)
                #     data_delay_df = pd.read_csv('D:\\Data_Delay_Alert\\Data_Delay_Alert.csv')
                #     data_delay_df['DC_PS_SENTI'].iloc[0] = 'Data delay'
                #     data_delay_df.to_csv('D:\\Data_Delay_Alert\\Data_Delay_Alert.csv', index=False)

                # else:
                #     time_delay_alert.write("")
                #     data_delay_df = pd.read_csv('D:\\Data_Delay_Alert\\Data_Delay_Alert.csv')
                #     data_delay_df['DC_PS_SENTI'].iloc[0] = 'No data delay'
                #     data_delay_df.to_csv('D:\\Data_Delay_Alert\\Data_Delay_Alert.csv', index=False)


                complete_df[['Senti_2003', 'Senti_2051', 'Senti_6760', 'Senti_9771']] = complete_df[
                    ['Senti_2003', 'Senti_2051', 'Senti_6760', 'Senti_9771']].astype(int)
                complete_styled_df = style_dataframe(complete_df)

                # update placeholders
                # summary_placeholder.dataframe(summary_df, width=5000)
                complete_placeholder.dataframe(complete_styled_df, width=5000)

                # Sleep for 3 seconds before the next update
                time.sleep(3)

            except Exception as e:
                print('Issue:', e)
                time.sleep(1)
                pass

except KeyError:
    # Handle the KeyError when the key is not found in session state
    st.error('User not Logged in')
    st.markdown('<span style="color: blue;">Please go to login in the side menu</span>', unsafe_allow_html=True)

except Exception as e:
    # Handle all other exceptions
    st.error(e)




