# Dependency extraction (EP-1027)

The dependency action preserves complete versions from the artifact filename, including custom suffixes such as `4.5.3.135-fav.1`, dotted names such as `4.5.2.211.FAV`, and build metadata. Native/Iris URLs remain unchanged. It does not infer the version from a host or directory, strip unknown suffixes, or treat a custom profile as audio.

Known platform/channel extraction and compact adjacent-URL boundaries are retained. An unrecognized filename has an empty version instead of an invented prefix. Consumers must still select and validate the source artifacts; parsing is not release authorization.

Run `python3 -m unittest discover -s .github/actions/dep -v`.
