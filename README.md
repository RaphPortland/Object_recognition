
## Goal : Find lost property through image recognition.

### 1. Extract pictures from a lost/found Blog. 
  I'm gonna take an exemple, *I lost my wallet lately.*
  On this blog we can find 10 pictures of lost things and places where lost things are kept.
  On this blog we can also find 1 picture named "reference", *it's an old picture of my wallet*. 
  We are going to compare this old picture with all the pictures from the lost and found blog and try to find where is it kept now.
  All these images are saved on a local disk. 

### 2. Image classification algorithms(open cv - feature matching).
  Compare images between them and find the ones with the best similirarities. Algorithm from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html
  
### 3. Print results 
Print URL(Homepage address link) of the image which match with the picture named "reference", *my wallet*. 
We are printing the URL(Homepage address link) because it contains information about the lost place (location, phone number of the lost and found center) and a picture of the item.
