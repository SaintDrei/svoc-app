# svoc-app
Python streamlit app for SVOC approval facilitation. 

# Agenda
* ~~Create loading loop~~
* ~~Auto-tag PIVOTS & SIBLINGS as PIVOT~~
* ~~Create timetaken function~~
* Create filter widget to search for clusters/records
* ~~Create export function~~
    * ~~Commit all edited rows to datatable~~
    * ~~Print out datatable as CSV~~
* Create BAT files for setup, init
* Separate rendering of view dependent on filtering or first approval.
* Optimize program by creating functions
* Eliminate duplicate tables inside while loop
* Eliminate endless sleep without st.write() on end of approval_wait loop
* Fix remarks input

## Optional Features
* Include dupe highlighting for QOL(Easier match spotting by glance)
* Create review function for all matching records
* Create approval suggestions based on current guidelines
* Create guideline widget on sidebar
* Stylized UI, colors for approve and reject button
* ~~Generate report: timetaken, cluster count, matched_row count;~~ export to separate CSV or text or copy button
* Progress bar to ~~show rows completed out of total matched_rows~~
* ~~Review cluster after a cluster loop~~

# UI Preview
![](img/Approval_UI.15.JPG)
