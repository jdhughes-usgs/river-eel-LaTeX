1. Create a tag for the commit using:

   ```
   git tag 'tagname' -m "your message for the tag"
   ```
   
   or if the tag already exists
   
   ```
   git tag -f 'tagname' -m "your message for the tag"
   ```
   
   or you can run `tagFromBranch.py` to create a tag using the version number (including the build number for the current bug-fix)
   
   ```
   python tagFromBranch.py
   ```
   
2. Push the commit using

	```
	git push -f --tags
	```
3. The latex document will show up as a download for the release with the tag name (`tagname`).