# Peloton to Strava to Garmin Converter tool

When using Peloton for indoor cycling workouts, users often share their activity data directly to Strava for broader tracking and social features; however, exporting these activities from Strava as TCX files frequently results in compatibility issues with Garmin Connect, leading to upload errors like “unsupported file type” or generic failures due to non-standard elements such as resistance data or malformed extensions. To address this, the provided Python-based tool processes the Strava-exported TCX file by removing invalid tags, rounding values to schema-compliant integers, and restructuring extensions, ensuring seamless recognition and import into Garmin Connect for accurate logging of metrics like heart rate, cadence, and power.

This Python tool does the conversion from the Strava Export. It cleans up the file so that Garmin recognizes it. 

The command line is:  FixTCX.py [-h] [-o OUTPUT_FILE] input_file

If you need more instructions...

Follow these step-by-step instructions to share a Peloton activity to Strava, export it as a TCX file, clean it using a Python script for compatibility, and then import it into Garmin Connect. This process addresses common issues like Garmin rejecting TCX files due to non-standard elements in Peloton data. Note that Peloton activities are indoor rides without GPS data, so the resulting file will reflect that.

Details here: [Converting and Importing a Peloton Activity to Garmin Connect via Strava](https://rodtrent.substack.com/p/converting-and-importing-a-peloton)

Want a version with a user interface (instead of one that uses a command-line)? See: [Streamlit-Powered Peloton to Garmin TCX Fixer: Say Goodbye to Upload Errors](https://github.com/rod-trent/JunkDrawer/tree/main/Peloton2Strava2Garmin)
