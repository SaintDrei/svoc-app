# svoc-app
Python streamlit app for SVOC approval facilitation. 

# Agenda
* Create filter widget to search for clusters/records
* Create BAT files for setup, init
* Separate rendering of view dependent on filtering or first approval.
* Optimize program by creating functions
* Fix preparePivots() to scan for unmarked pivots by selecting recordid==matchid==recordid and recordid==matchid:
    * Prepare Cluster Table
    * check for records with matchid!=clusterid
    * get the record with matchid==recordid
    * tag as sibling and pass to pivots table
* Create separate Second Approval Script to:
    * Replace Approval writing
    * Additional Checkbox to tag Errors  or autotag them based on changes
* Fix untagged pivot showing up as matched record

## Optional Features
* Include dupe highlighting for QOL(Easier match spotting by glance)
* Create approval suggestions based on current guidelines
* Create guideline widget on sidebar
* Stylized UI, colors for approve and reject button
* Progress bar to ~~show rows completed out of total matched_rows~~
* Allow edits during Cluster Review
* Create checkboxes for common remarks


## Bugs
* Duplicate Next Button
* Remarks not clearing on next record
* Minor delay in viewing next record

# UI Preview
![](img/9.1.JPG)
![](img/9.2.JPG)
![](img/9.3.JPG)
![](img/9.4.JPG)
![](img/9-cluster-review.JPG)
![](img/9-end.JPG)