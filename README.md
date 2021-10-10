# student_dropout
Student Dropout Prediction


![Project Image](project-image-url)

> This README file describe the overview of the Student Dropout Prediction Project.

---

### Table of Contents


- [Description](#description)
- [Dataset](#dataset)
- [Dataset description](#dataset-description)
- [Proposed steps](#proposed-steps)
- [References](#references)
- [License](#license)
- [Author Info](#author-info)

---

## Description

Massive Open Online Courses (MOOCs) can provide broad and potentially scalable platforms for learning. Truly open MOOCs allow students around the world to enroll in any course that piques their interest or meets professional needs. Most of the available MOOCs are free, and many stay open perpetually even after their official offerings are complete thus allowing students to use them as a regular reference point or as a social platform. One major concern with MOOCs is that they have extremely high rates of dropout. More than 85% of students who register for a MOOC quit without completing it . Prior research has indicated that student dropout in MOOCs, and student performance more generally, is highly correlated with features of the students’ online activities such as viewing lectures or attempting mastery quizzes.

Building predictive models of student success has emerged as a core task in the fields of learning analytics and educational data mining. As MOOCs have grown, so has this need for effective and reliable machine learning models of complex student behavior patterns which identify students likely to drop out in order to provide appropriate interventions or support. The present work is concerned with building and evaluating models to address the following task: The Model Selection Task (MST): Given the full set of learner data in N courses up to time t, find the best of k methods to predict learner dropout at time t + 1.

 Students’ high dropout rate on MOOC platforms (e.g., Coursera) has been heavily criticized, and predicting their likelihood of dropout would be useful for maintaining and encouraging students' learning activities. In this competition, you are challenged to build a predictor that can predict the chance that a student will drop out of an enrolment after observing his/her early course activities. In particular, you have access to the student's course-relevant activities, such as working on course assignments, watching course videos, accessing the course wiki, etc



[Back To The Top](#student_dropout)

#### Dataset

the data set used for project is taken from Student Dropout Prediction Challenge hosted on kaggle.

[Back To The Top](#student_dropout)

#### Dataset description	

	 enrollment_id - an anonymous id unique to a given enrollment of a student
	 
	 dropout_prob - the probability that the student drop out of the enrollment 
	 
	time - the time when the event happens 

We define 7 different event types:

	 -problem - working on course assignments
	 
	 – video - watching course videos. 
	 
	- access - accessing other course objects except videos and assignments 

	- wiki - accessing the course wiki 

	- discussion - accessing the course forum

	 - navigation - navigating to other part of the course.
	 
	 - page_close - closing the web page

		
		
[Back To The Top](#student_dropout)

---

## Proposed Steps

####	1.	EDA
	Null value:

	A NULL value is a special marker to indicate that a data value does not exist in the database
	we can Finding null  in dataset by using pandas 

	ex: data_df.isnull().sum() 

	which display the sum of null values in sequence
![Image1](images/first.png)

	Handling null values:

 	1.Delete rows which contains the null values:
	This method commonly used to handle the null values. Here, we either delete a particular 
	row if it has a null value for a particular feature and a  particular column 
	if it has more than 70-75% of missing values. This method is advised only when there are 
	enough samples in the data set. One has to make sure that after we have deleted 
	the data, there is no addition of bias. Removing the data will lead to loss of information 
	which will not give the expected results while predicting the output.

	2.Replacing With Mean/Median/Mode:
	This strategy can be applied on a feature which has numeric data like the age of a person 
	or the ticket fare. We can calculate the mean, median or mode of the feature and 
	replace it with the missing values. This method is also called as leaking the data while 
	training. Another way is to approximate it with the deviation of neighbouring values. 
	This works better if the data is linear.in our dataset MOOC_Visual we dont have any null value.


	Target label:
	Target: final output you are trying to predict, also know as y . It can be categorical 
	(sick vs non-sick) or continuous (price of a house). Label:true outcome of the target. 
	In supervised learning the target labels are known for the trainining dataset but not for the test.
	in student droup out dataset the data is Unbalanced. if data in unbalance then machine learning 
	algorithm may get bias to this kind of output.
	we can balance data by using unsampling or downsampling
	for downsampling we have NearMiss  and for unsampling we have SMOTETomek

	downsampling :
	if x,y  is having independent and dependent dataset where y has 9:1 ration output and if total
	no of rows is 1000 ,by using NearMiss then the no of rows will be 200 , where ratio of the data 
	will become 5:5 for the output y.
	Code :
	 from imblearn.onder_sampling import NearMiss
	 nm = NearMiss(random_state=42)
	 x_res,y_res = nm.fit_sample(x,y)

	Upsampling:
	 if x,y  is having independent and dependent dataset where y has 9:1 ration output and if
	  total no of rows is 1000 ,by using SMOTETomek then the number of ratio will 
	  be 5:5 in ouput .but the rows will be increase.
	Code:
	 from imblearn.combine import SMOTETomek
	 smk = SMOTETomek(random_state=42)
	 x_res,y_res = smk.fit_sample(x,y)

	 our dataset MOOC_Visual  need to treated by any one of the technique
![Image2](images/second.png)


	Distribution of course drop rate:
	seeing the ratio on graph we can identify which cource having the high droping persent
	in MOOC_Visual data set drop rate of certain cource is very high
![Image3](images/third.png)


	Present days:
	As the Number of Present Days increases, No. of student Droping from course decreases we can see 
	this in graphically .
	When the stutent are  concentrating  in studies then the chance of droping the course will be 
	automaticaly low.
![Image4](images/fourth.png)

	
	Heatmap:
	heatmap is a graphical representation of data that uses a system of color-coding to represent 
	different values.Heatmaps are used to show relationships between two variables, one plotted 
	on each axis. By observing how cell colors change across each axis,you can observe if there are
	any patterns in value for one or both variables.
![Image5](images/fifth.png)
####	2.	Feature Engineering

#####	What is an outlier:
	The value lies an abnormal distance from all values is called outlier.
	It can be caused by measurement or execution error. The analysis of outlier data is referred to as outlier analysis or outlier mining.
	
#####	Identifying Outliers: 
	There are many ways to identifying outliers, here we are observing outliers using describe() method.
	
#####	Data describing: 
	Using the code data.describe(), we get the statistical details of minimum, maximum, mean, 25%, 75%, etc.

![01 - Describe](https://user-images.githubusercontent.com/66309235/102394195-6514bb80-3fff-11eb-95a2-ac31b261296a.PNG)
	
	From the data describing, we observed that the value of (MEAN – 25%)/(25% – MIN) or (75% – MEAN)/(MAX – 75%) is less than 0.5,
	then there are chances of existing outlier.
	Now the next task is which method we use for removing outliers.
	One of the methods is Z-score.
	
#####	Z-score Method:
	Z score is also called standard score; it tells how many standard deviations away a data point is from the mean.
	If the data is normally distributed, then
	68% of the data points lie between +/- 1st standard deviation
	95% of the data points lie between +/- 2nd standard deviation
	99.7% of the data points lie between +/- 3rd standard deviation
	
![02 - z score](https://user-images.githubusercontent.com/66309235/102389431-211eb800-3ff9-11eb-9d39-762038869b50.jpeg)

#####	Outlier : If the z score of a data point is away from 3rd standard deviation, that can be an outlier.
#####	Math Formula : Z_score = (x – x_mean) / x_std
	
![03 - describe](https://user-images.githubusercontent.com/66309235/102389461-2b40b680-3ff9-11eb-85b6-9554c00d049f.JPG)
	
	We can apply Z-score method mostly when the data is normally distributed.
	But most of the column values are large between MAX and 75%, and those seem to be right-skewed (Not normal distributed).
	We plot the graph distplot() for each column. 

![04](https://user-images.githubusercontent.com/66309235/102389680-71961580-3ff9-11eb-8ba2-d3c4eae3a0e5.JPG)

![access and navigate](https://user-images.githubusercontent.com/66309235/102389659-680cad80-3ff9-11eb-9503-1405ea9eabd0.JPG)

	By this graph we can identify whether the column is skewed or not. As we observed most of the columns are right-skewed.
	If we apply 3rd Standard deviation method, there are chances of losing the significant data since the data distribution is skewed.
	We have to find another method to deal with these outliers so that we should not lose the significant data.
	So, we try to apply the IQR (Inter-Quartile Range) method by using the technic Extreme Outliers.

#####	Interquartile Range (IQR) Method:
	The IQR is a measure of variability, based on dividing a data set into quartiles.
	Quartiles divide a rank-ordered data set into four equal parts.
	The values that divide each part are called the first, second, and third quartiles; and they are denoted by Q1, Q2, and Q3, respectively.
	Q1 is the first quartile of the data i.e., 25% of the data lies between minimum and Q1.
	Q2 is the median value in the set.
	Q3 is the third quartile of the data, i.e., 75% of the data lies between minimum and Q3.
	IQR = Q3 – Q1, is called the Inter-Quartile Range.
	
![06 - IQR](https://user-images.githubusercontent.com/66309235/102389754-912d3e00-3ff9-11eb-94b7-c05401092a05.jpeg)

	To detect the outliers using this method, we define a new range, let’s call it decision range.
#####	Lower Bound: (Q1 - 1.5 * IQR)
#####	Upper Bound: (Q3 + 1.5 * IQR)
#####	Outlier: Any data point less than the Lower Bound or more than the Upper Bound is considered as an outlier.
	
![06 - acess](https://user-images.githubusercontent.com/66309235/102389798-a1451d80-3ff9-11eb-83c2-6880ba907d32.JPG)![07 - navigate](https://user-images.githubusercontent.com/66309235/102389815-a7d39500-3ff9-11eb-9909-dc636d784f4b.JPG)

	Since there is a huge variation among MAX values in the columns, we go for univariate analysis  for removing outliers. 
	
	From the Data description, we identified that it is enough to remove outliers for the columns
	"access", "discussion", "navigate", "page_close", "problem", "video", "wiki", "proccess_period", "present_days", "effective_time".
	We plotted the graphs with Boxplot() and Probplot() methods for each column and from these graphs also we observed that most columns are right-skewed
	and also there is a huge difference between MAX and 75% value, we tried to find extreme upper bound value.
	We have updated the data frame with the data whose values are less than the extreme upper bound value.
	We have continued this for all the above columns which we have considered.

![08 - access](https://user-images.githubusercontent.com/66309235/102389841-b457ed80-3ff9-11eb-877f-51f02e1886be.JPG)
![09 - navigate](https://user-images.githubusercontent.com/66309235/102389862-bcb02880-3ff9-11eb-9861-2494bfd281df.JPG)
	
	After removing outliers still, our original continuous data do not follow the bell curve,
	we can log transform this data to make it as “normal” as possible so that the statistical analysis results from this data become more valid.
	
#####	Log Transformation:
	The log transformation can be used to make highly skewed distributions less skewed.
	This can be valuable both for making patterns in the data more interpretable and for helping to meet the assumptions of inferential statistics.
	
![10 - before and after log transformation](https://user-images.githubusercontent.com/66309235/102389889-c6399080-3ff9-11eb-9a7e-092bc93a2984.JPG)

![11 - before and after log transformation](https://user-images.githubusercontent.com/66309235/102389917-ccc80800-3ff9-11eb-8309-2d89bb3abf11.JPG)


####	3 std method 
	.	 Manual Removal
	•	Scaling (Standard Scaling) 
####	3. Feature Selection
	•	PCA
	•	Heat Map correlation
Note: Only 23 Features were present (This step was for experimental purpose) 
####	4.Model Building
•	Hold Out Method (Splitting Dataset into train and test part) 
•	Upsampling (Resampling Approach)

####	5.Model Evaluation Metrics

####	6. Creating Binary file (Pickle file)

####	7.Model Deployment:
•	Expose model via a FLASK API
•	Deploy new model to small subset of users to ensure everything goes smoothly, then roll out to all users

####	8.Ongoing model maintenance:
•	Understand that changes can affect the system in unexpected ways
•	Periodically retrain model to prevent model staleness
•	If there is a transfer in model ownership, educate the new team


[Back To The Top](#student_dropout)


#### API Reference

```html
    <p>dummy code</p>
```
[Back To The Top](#student_dropout)

---


---

## References
[Back To The Top](#student_dropout)

---

## License

MIT License

Copyright (c) [2017] [James Q Quick]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[Back To The Top](#student_dropout)

---

## Author Info

- Twitter - []()
- Website - []()

[Back To The Top](#student_dropout)
