import streamlit as st
import pandas as pd

st.set_page_config(
    page_title='SWBSA | Sets by Day',
    page_icon='⚙️',
    layout='wide'
)


st.caption('VACAYZEN')
st.title('SWBSA Sets by Day')
st.info('The Vacayzen-submitted sets scheduled each day in the South Walton Beach Service Association system.')


sets_file = st.file_uploader('Export Rentals by Day | integraRental','CSV')

if sets_file is None:
    with st.expander('How to pull the report'):
        st.write('[integraRental | Vendor Submissions](https://swbsa-rental.integrasoft.net/Login.aspx)')
        st.info('Pull from January 1 through December 31.')
        st.video('https://youtu.be/2BMCv0ygLbg')

else:
    sets = pd.read_csv(sets_file, index_col=False)

    sets.RentalAgreementStartDate = pd.to_datetime(sets.RentalAgreementStartDate).dt.date
    sets.RentalAgreementEndDate   = pd.to_datetime(sets.RentalAgreementEndDate).dt.date

    with st.container(border=True):
        l, r = st.columns(2)
        start = l.date_input('**Start Date** of Range')
        end   = r.date_input('**End Date** of Range', value=start, min_value=start)
    dates = pd.date_range(start, end)
    
    def GetDatesFromRange(row):
        dates = pd.date_range(row.RentalAgreementStartDate, row.RentalAgreementEndDate, normalize=True).values
        return set(map(lambda x: pd.to_datetime(x).date(), dates))
    
    sets['Dates'] = sets.apply(GetDatesFromRange, axis=1)

    results = []

    for date in dates:

        datesets = sets[[date.date() in d for d in sets.Dates]]
        datesets = datesets.rename(columns={'Description':'Beach Access', 'Quantity':str(date.date())})
        datesets = datesets[datesets.RentalCompanyName == 'VACAYZEN']
            
        result = datesets.groupby('Beach Access', group_keys=True)[str(date.date())].apply(sum)

        results.append(result)
    
    final = pd.concat(results, axis=1)

    st.dataframe(final, use_container_width=True)