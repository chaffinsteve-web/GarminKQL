# Peloton to Strava to Garmin Converter tool

When using Peloton for indoor cycling workouts, users often share their activity data directly to Strava for broader tracking and social features; however, exporting these activities from Strava as TCX files frequently results in compatibility issues with Garmin Connect, leading to upload errors like “unsupported file type” or generic failures due to non-standard elements such as resistance data or malformed extensions. To address this, the provided Python-based tool processes the Strava-exported TCX file by removing invalid tags, rounding values to schema-compliant integers, and restructuring extensions, ensuring seamless recognition and import into Garmin Connect for accurate logging of metrics like heart rate, cadence, and power.

Follow these step-by-step instructions to share a Peloton activity to Strava, export it as a TCX file, clean it using a Python script for compatibility, and then import it into Garmin Connect. This process addresses common issues like Garmin rejecting TCX files due to non-standard elements in Peloton data. Note that Peloton activities are indoor rides without GPS data, so the resulting file will reflect that.

https://open.substack.com/pub/rodtrent/p/converting-and-importing-a-peloton
