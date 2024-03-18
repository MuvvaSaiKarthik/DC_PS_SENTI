import streamlit as st
import datetime
import pandas as pd
import time

st.set_page_config(layout='wide')

def style_dataframe(df):
    return df.style.applymap(
        lambda x: 'color: green' if x > 0 else ('color: red' if x < 0 else 'color: black'),
        subset=['Available', 'DC_Margin', 'DCpcnt', 'PL_Margin', 'DC_PSbyPL']
    )

# style yellow if values between 80 and 90 like (351, 401),
# style red if value greater than 90 like else white
def style_dataframe_bg(df):
    return df.style.applymap(
        lambda x: 'background-color: yellow' if ((x > 80) & (x < 90)) else ('background-color: red; color: white' if x >= 90 else 'background-color: white'),
        subset=['DCpcnt']
    )


def time_difference_in_minutes(dt1, dt2):
    timedelta = dt2 - dt1
    return (timedelta.total_seconds() // 60)


try:
    if st.session_state["my_input"] == 'VIKABH':
        st.title('DC PS PL COMPARISON')
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
                complete_df = pd.read_csv('D:\\streamlit_input_files\\dc_ps_pl_comparison\\DC_ps_pl_compare.csv')
                dt_time_frame = complete_df['DT'].iloc[0]
                dt_time_frame = dt_time_frame.split('_')[0].upper()
                del complete_df['DT']

                dt_time_frame = pd.to_datetime(dt_time_frame)
                dt_time_frame = dt_time_frame.strftime('%Y-%m-%d %H:%M:%S')
                dt_time_frame = pd.to_datetime(dt_time_frame)
                current_time_dt = pd.to_datetime(current_time)
                time_diff_min = time_difference_in_minutes(current_time_dt, dt_time_frame)
                time_diff_min = abs(time_diff_min)

                dc_dt_time_frame = complete_df['DC_DT'].iloc[0]
                del complete_df['DC_DT']

                # Update time_display placeholder
                time_display.write(
                    f'CT {current_time}   |   DT {dt_time_frame}   |   DC_DT {dc_dt_time_frame}', format='md')

                if time_diff_min > 3:
                    time_delay_alert.markdown('<span style="color: red">Data delay greater than 2 minutes!</span>',
                                              unsafe_allow_html=True)
                    data_delay_df = pd.read_csv('D:\\Data_Delay_Alert\\Data_Delay_Alert.csv')
                    data_delay_df['DC_PS_PL_COMPARISON'].iloc[0] = 'Data delay'
                    data_delay_df.to_csv('D:\\Data_Delay_Alert\\Data_Delay_Alert.csv', index=False)
                else:
                    time_delay_alert.write("")
                    data_delay_df = pd.read_csv('D:\\Data_Delay_Alert\\Data_Delay_Alert.csv')
                    data_delay_df['DC_PS_PL_COMPARISON'].iloc[0] = 'No data delay'
                    data_delay_df.to_csv('D:\\Data_Delay_Alert\\Data_Delay_Alert.csv', index=False)


                complete_df[['Available', 'DC_Margin', 'DCpcnt', 'PL_Margin', 'DC_PSbyPL']] = round(
                    complete_df[['Available', 'DC_Margin', 'DCpcnt', 'PL_Margin', 'DC_PSbyPL']], 2)

                complete_df.fillna(0, inplace=True)
                complete_df['DCpcnt'] = complete_df['DCpcnt'].astype(int)

                complete_df_styled = style_dataframe_bg(complete_df)

                # update placeholders
                complete_placeholder.dataframe(complete_df_styled, width=5000)

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


