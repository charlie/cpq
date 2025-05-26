1. Download the variable-rate non-prepayment, non-busines TILs from
https://uw.co.uk/legal/terms-conditions/energy-tariff-information into
./TILs/residential/credit
2. Extract the HTML containing the links to the fixed-rate TILs from your
browser (web inspector or similar), use it to update the value of the
`fixed_tariff_html` variable in fixed_til_downloader.py, and run that program
to download the fixed-rate TILs.
3. Run tarifftable.py and save the output to a .csv file.
4. Use the .csv file to update https://docs.google.com/spreadsheets/d/1eJ6f_7Cro7BMb-1TXku_Jn739Dik62_IuN9T606s8IQ/edit?gid=2141275997#gid=2141275997
5. Sort the Google sheet by the first three columns
