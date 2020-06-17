import sys
import pandas as pd
import numpy as np

from time import sleep
from PyQt5.QtWidgets import *
from PyQt5 import uic
form_class = uic.loadUiType("untitled.ui")[0]
 
class MyWindow(QDialog, form_class):
	   
   def __init__(self):
       global meter # meter 상태이므로 전역변수
       global fname # 파일 경로, 지역변수 사용하는게 좋은데 편의상 전역변수로 사용하는중
       meter=0
       fname=" "
       super().__init__()
       self.setupUi(self)
       self.pushButton.clicked.connect(self.btn_clicked)
       self.pushButton_2.clicked.connect(self.btn2_clicked)
       self.radioButton.clicked.connect(self.meterbtn1)
       self.radioButton_2.clicked.connect(self.meterbtn2)
       self.radioButton_3.clicked.connect(self.meterbtn3)
#raweraser
	   
   def vacheck(value,series,count): #Series 인자로 받은 후 이상치값 분석, 해당함수를 n번 돌려야함 부하가 클것으로 예상
       anum=count/4
       bnum=anum*3
       print(anum,bnum)
       valuech=series[bnum]-series[anum]
       if(value<(series[anum]-valuech)):
        return false
       elif(value>(series[bnum]+valuech)):
        return false
       else:
        return true
	 
   def scheck(self,series,count): #Series 인자로 받은 후 이상치값 분석, return 값보다 작으면 이상치
       if count==0:
        return 0	   
       anum=int(count/4)
       bnum=anum*3
     #  print(anum,' ',bnum)
       valuech=series[bnum]-series[anum]
   #    print(series)    
       value=series[anum]-(2*valuech)
	   
       return value	 
  	  	   
   def bcheck(self,series,count): #Series 인자로 받은 후 이상치값 분석, return 값보다 작으면 이상치
       if count==0:
        return 0	   
       anum=int(count/4)
       bnum=anum*3
     #  print(anum,' ',bnum)
       valuech=series[bnum]-series[anum]
   #    print(series)    
       value=series[bnum]+(2*valuech)
	   
       return value	 	   
	   
   def meterbtn1(self):
       global meter
       meter=1
	   
   def meterbtn2(self):
       global meter
       meter=2

   def meterbtn3(self):
       global meter
       meter=3
	   
   def printall(self,ertype,mid,day,num) :
       if ertype==1 :
        self.textBrowser.append(mid+' 의 '+day+' 날짜의 데이터 갯수는 '+num+' 개 입니다.')
        self.textBrowser.append('갯수가 정상 범위가 아니므로 확인이 필요합니다.')
        self.textBrowser.append('----------------------------------------------------------------------')	   
       elif ertype==2 :
        self.textBrowser_2.append(mid+' 의 '+day+' 날짜에 숫자가 아닌 데이터가 있습니다.')
        self.textBrowser_2.append('----------------------------------------------------------------------')	        
       elif ertype==3 :	
        self.textBrowser_2.append(mid+' 의 '+day+' 날짜의 데이터값이 이상합니다. 확인이 필요합니다.')
        self.textBrowser_2.append('----------------------------------------------------------------------')	   
	   
   def glp(self): #G,AE,S타입 LP검침
       data=pd.read_csv(fname[0])
       data=data.replace(['"','='],['',''],regex=True) # 특수문자 제거
       data2=data[[" LTE SysT"," Meter ID"," CTime"," FAP"," LARAP"," LERAP"," AP"]]
       data2.rename(columns={' FAP':'FEP'},inplace=True) #이하 처리를 위한 행제목 변경
       data2.rename(columns={' LARAP':'LARAP'},inplace=True)
       data2.rename(columns={' LERAP':'LERAP'},inplace=True)
       data2.rename(columns={' AP':'AP'},inplace=True)
       data2.rename(columns={' Meter ID':'MeterID'},inplace=True)
       data2.rename(columns={' CTime':'CTime'},inplace=True)
       data2['FEP']=pd.to_numeric(data2['FEP'],errors='coerce')
       #print(data2['FEP'].quantile(0.5),'FEP')
	   
       data6=data2.drop_duplicates('MeterID',keep='first') # 미터정보만 남김
       data6.MeterID.count() #전체 미터 갯수
       data6.MeterID.values #전체 미터 번호
       data6=data6.reset_index(drop=True)
	   
       data7=data2[['CTime']] # 시간축 데이터만 잘라냄
       data7['CTime']=data7['CTime'].apply(lambda e:e.split()[0]) # 블록단위로 자름
       data7=data7.drop_duplicates('CTime',keep='first')
       data7.sort_values('CTime')
       data7=data7.reset_index(drop=True)
	   
       for i in range(0,data6.MeterID.count()):
        data8=data2[(data2.MeterID==data6.MeterID[i])]
        data8=data8.sort_values(by='FEP',ascending=True)
        data8=data8.reset_index(drop=True)
        o=data8.FEP.count()		
        svalue=self.scheck(data8.FEP.values,o)
        bvalue=self.bcheck(data8.FEP.values,o)
        print(svalue)		   
        print(bvalue)		   
        kk=bvalue-svalue
        if(bvalue==0 & svalue==0):
         kk=-1		
        sleep(0.1) #제대로 작동안하는듯하다	   
        for j in range(0,data7.CTime.count()):
         data8=data2[(data2.MeterID==data6.MeterID[i])] # 아래의 경우 2*o로 사용가능
         data8=data8[(data8['CTime'].str.contains(data7.CTime[j]))]
         data8=data8.drop_duplicates('CTime',keep='first') # 시간 중복데이터 제거 	 
         k=data8.FEP.count() # 하루치 LP갯수
         data8['FEP']=pd.to_numeric(data8['FEP'],errors='coerce') #쓰레기값 여부 확인을 위해 datatype 변경
         data8['LARAP']=pd.to_numeric(data8['LARAP'],errors='coerce')
         data8['LERAP']=pd.to_numeric(data8['LERAP'],errors='coerce')
         data8['AP']=pd.to_numeric(data8['AP'],errors='coerce')          
         # print(data8) #데이터 맞게 가지고 있음 
         if k!=96: #일일 LP 개수가 정상이 아닐경우 체크
          if k!=0:  
            self.printall(1,data6.MeterID[i],data7.CTime[j],str(k))
			
         check=data8['FEP'].isnull().sum()+data8['LARAP'].isnull().sum()+data8['LERAP'].isnull().sum()+data8['AP'].isnull().sum()
         if check>0:
          self.printall(2,data6.MeterID[i],data7.CTime[j],str(k))				
         else:	
          if kk==-1 :
           data10=data8[data8['FEP']>1000000]
          else :		   
           data10=data8[data8['FEP']>bvalue]
           data10=data10+data8[data8['FEP']<svalue]	 
           data10=data10+data8[data8['FEP']>1000000] #FEP의 쓰레기값 조건 범위 확인		 
           data10=data10+data8[data8['FEP']<0] #FEP의 쓰레기값 조건 범위 확인
           data10=data10+data8[data8['LARAP']>1000000]
           data10=data10+data8[data8['LARAP']<0]		 
           data10=data10+data8[data8['LERAP']>1000000]
           data10=data10+data8[data8['LERAP']<0]
           data10=data10+data8[data8['AP']>1000000]
           data10=data10+data8[data8['AP']<0]		
          ''' print(data11) # 테스트용 코드
      #     if data11.empty==False:
     #   	   print(data6.MeterID[i]+"!!!!!")
      #  	   #print(data10)
     #      else:
      #  	   print(data6.MeterID[i])'''
          if data10.empty==False: #하나라도 쓰레기값 범위인 경우
           self.printall(3,data6.MeterID[i],data7.CTime[j],str(k))	 

   def elp(self): #E타입 LP검침
       data=pd.read_csv(fname[0])
       data=data.replace(['"','='],['',''],regex=True) # 특수문자 제거
       data2=data[[" LTE SysT"," Meter ID"," MTime"," FAP"," WC"]]
       data2.rename(columns={' FAP':'FEP'},inplace=True) #이하 처리를 위한 행제목 변경
       data2.rename(columns={' WC':'WC'},inplace=True)
       data2.rename(columns={' Meter ID':'MeterID'},inplace=True)
       data2.rename(columns={' MTime':'CTime'},inplace=True)
       data2['FEP']=pd.to_numeric(data2['FEP'],errors='coerce')
	   
       data6=data2.drop_duplicates('MeterID',keep='first') # 미터정보만 남김
       data6.MeterID.count() #전체 미터 갯수
       data6.MeterID.values #전체 미터 번호
       data6=data6.reset_index(drop=True)
	   
       data7=data2[['CTime']] # 시간축 데이터만 잘라냄
       data7['CTime']=data7['CTime'].apply(lambda e:e.split()[0]) # 블록단위로 자름
       data7=data7.drop_duplicates('CTime',keep='first')
       data7.sort_values('CTime')
       data7=data7.reset_index(drop=True)
	   
       for i in range(0,data6.MeterID.count()):
        data8=data2[(data2.MeterID==data6.MeterID[i])]
        data8=data8.sort_values(by='FEP',ascending=True)
        data8=data8.reset_index(drop=True)
        o=data8.FEP.count()
        svalue=self.scheck(data8.FEP.values,o)
        bvalue=self.bcheck(data8.FEP.values,o)
        print(svalue)		   
        print(bvalue)		   
        kk=bvalue-svalue
        if(bvalue==0 & svalue==0):
         kk=-1			
        sleep(0.1) #제대로 작동안하는듯하다	   
        for j in range(0,data7.CTime.count()):		
         data8=data2[(data2.MeterID==data6.MeterID[i])]
         data8=data8.sort_values(by='FEP',ascending=True)
         data8=data8.reset_index(drop=True)		 	
         data8=data2[(data2.MeterID==data6.MeterID[i])] # 아래의 경우 2*o로 사용가능
         data8=data8[(data8['CTime'].str.contains(data7.CTime[j]))]
         data8=data8.drop_duplicates('CTime',keep='first') # 시간 중복데이터 제거 	 
         k=data8.FEP.count() # 하루치 LP갯수
         data8['FEP']=pd.to_numeric(data8['FEP'],errors='coerce') #쓰레기값 여부 확인을 위해 datatype 변경
         data8['WC']=pd.to_numeric(data8['WC'],errors='coerce')   
          # print(data8) #데이터 맞게 가지고 있음 
         if k!=96: #일일 LP 개수가 정상이 아닐경우 체크
          if k!=0:  
           self.printall(1,data6.MeterID[i],data7.CTime[j],str(k))
         check=data8['FEP'].isnull().sum()+data8['WC'].isnull().sum()
         if check>0:
          self.printall(2,data6.MeterID[i],data7.CTime[j],str(k))				
         else:	
          if kk==-1 :
           data10=data8[data8['FEP']>1000000]
          else :		   
           data10=data8[data8['FEP']>bvalue]
           data10=data10+data8[data8['FEP']<svalue]	 
           data10=data10+data8[data8['FEP']>1000000] #FEP의 쓰레기값 조건 범위 확인		 
           data10=data10+data8[data8['FEP']<0] #FEP의 쓰레기값 조건 범위 확인
           data10=data10+data8[data8['WC']>1]
           data10=data10+data8[data8['WC']<0]		 		
          if data10.empty==False: #하나라도 쓰레기값 범위인 경우
           self.printall(3,data6.MeterID[i],data7.CTime[j],str(k))	

   def grg(self): #G,AE타입 정기검침
       data=pd.read_csv(fname[0])
       data=data.replace(['"','='],['',''],regex=True) # 특수문자 제거
       data2=data[[" Meter ID"," Received Time"," APT1"," APT2"," RPT"," LPT"," PFT"]]
       data2.rename(columns={' APT1':'APT1'},inplace=True) #이하 처리를 위한 행제목 변경
       data2.rename(columns={' APT2':'APT2'},inplace=True)
       data2.rename(columns={' RPT':'RPT'},inplace=True)	   
       data2.rename(columns={' LPT':'LPT'},inplace=True)	   
       data2.rename(columns={' PFT':'PFT'},inplace=True)	   
       data2.rename(columns={' Meter ID':'MeterID'},inplace=True)
       data2.rename(columns={' Received Time':'CTime'},inplace=True)          
#rrrr
       data2['APT1']=pd.to_numeric(data2['APT1'],errors='coerce') #쓰레기값 여부 확인을 위해 datatype 변경
       data2['APT2']=pd.to_numeric(data2['APT2'],errors='coerce')
       data2['RPT']=pd.to_numeric(data2['RPT'],errors='coerce')
       data2['LPT']=pd.to_numeric(data2['LPT'],errors='coerce')
       data2['PFT']=pd.to_numeric(data2['PFT'],errors='coerce')
	   
       data6=data2.drop_duplicates('MeterID',keep='first') # 미터정보만 남김
       data6.MeterID.count() #전체 미터 갯수
       data6.MeterID.values #전체 미터 번호
       data6=data6.reset_index(drop=True)
	   
       data7=data2[['CTime']] # 시간축 데이터만 잘라냄
       data7['CTime']=data7['CTime'].apply(lambda e:e.split()[0]) # 블록단위로 자름
       data7=data7.drop_duplicates('CTime',keep='first')
       data7.sort_values('CTime')
       data7=data7.reset_index(drop=True)
	   
       for i in range(0,data6.MeterID.count()):
        for j in range(0,data7.CTime.count()):
         data8=data2[(data2.MeterID==data6.MeterID[i])] # 아래의 경우 2*o로 사용가능
         data8=data8[(data8['CTime'].str.contains(data7.CTime[j]))]
#         data8=data8.drop_duplicates('CTime',keep='first') # 시간 중복데이터 제거 
         k=data8.APT1.count() # 하루치 LP갯수
        
         if k!=6: #일일 LP 개수가 정상이 아닐경우 체크
          if k!=0:  
           if k!=12:
            self.printall(1,data6.MeterID[i],data7.CTime[j],str(k))

         check=data8['APT1'].isnull().sum()+data8['APT2'].isnull().sum()+data8['RPT'].isnull().sum()+data8['LPT'].isnull().sum()+data8['PFT'].isnull().sum()
         if check>0:
            self.printall(2,data6.MeterID[i],data7.CTime[j],str(k))
         else :			
          data10=data8[data8['APT1']>1000000] #FEP의 쓰레기값 조건 범위 확인
          data10=data10+data8[data8['APT1']<0] #FEP의 쓰레기값 조건 범위 확인
          data10=data10+data8[data8['APT2']>1000000]
          data10=data10+data8[data8['APT2']<0]		 
          data10=data10+data8[data8['RPT']>1000000]
          data10=data10+data8[data8['RPT']<0]
          data10=data10+data8[data8['LPT']>1000000]
          data10=data10+data8[data8['LPT']<0]		 
          data10=data10+data8[data8['PFT']>1]
          data10=data10+data8[data8['PFT']<-1]	
		 
          if data10.empty==False: #하나라도 쓰레기값 범위인 경우
            self.printall(3,data6.MeterID[i],data7.CTime[j],str(k)) 
				
   def erg(self): #E타입 정기검침
       data=pd.read_csv(fname[0])
       data=data.replace(['"','='],['',''],regex=True) # 특수문자 제거
       data2=data[[" Meter ID"," Received Time"," SAP"," Status"]]
       data2.rename(columns={' SAP':'SAP'},inplace=True) #이하 처리를 위한 행제목 변경
       data2.rename(columns={' Status':'Status'},inplace=True)   
       data2.rename(columns={' Meter ID':'MeterID'},inplace=True)
       data2.rename(columns={' Received Time':'CTime'},inplace=True)          

       data6=data2.drop_duplicates('MeterID',keep='first') # 미터정보만 남김
       data6.MeterID.count() #전체 미터 갯수
       data6.MeterID.values #전체 미터 번호
       data6=data6.reset_index(drop=True)
	   
       data7=data2[['CTime']] # 시간축 데이터만 잘라냄
       data7['CTime']=data7['CTime'].apply(lambda e:e.split()[0]) # 블록단위로 자름
       data7=data7.drop_duplicates('CTime',keep='first')
       data7.sort_values('CTime')
       data7=data7.reset_index(drop=True)
	   
       for i in range(0,data6.MeterID.count()):
        for j in range(0,data7.CTime.count()):
         data8=data2[(data2.MeterID==data6.MeterID[i])] # 아래의 경우 2*o로 사용가능
         data8=data8[(data8['CTime'].str.contains(data7.CTime[j]))]
#         data8=data8.drop_duplicates('CTime',keep='first') # 시간 중복데이터 제거 
         k=data8.SAP.count() # 하루치 LP갯수
        
         if k!=6: #일일 LP 개수가 정상이 아닐경우 체크
          if k!=0:  
            self.printall(1,data6.MeterID[i],data7.CTime[j],str(k))
         data8['SAP']=pd.to_numeric(data8['SAP'],errors='coerce') #쓰레기값 여부 확인을 위해 datatype 변경
         data8['Status']=pd.to_numeric(data8['Status'],errors='coerce')   

         check=data8['SAP'].isnull().sum()+data8['Status'].isnull().sum()
         if check>0:
            self.printall(2,data6.MeterID[i],data7.CTime[j],str(k))
          
         else :
          data10=data8[data8['SAP']>1000000] #SAP의 쓰레기값 조건 범위 확인
          data10=data10+data8[data8['SAP']<0]
          data10=data10+data8[data8['Status']!=1]	 
          if data10.empty==False: #하나라도 쓰레기값 범위인 경우
            self.printall(3,data6.MeterID[i],data7.CTime[j],str(k))	      
		   
   def srg(self): #S타입 정기/현재검침
       data=pd.read_csv(fname[0])
       data=data.replace(['"','='],['',''],regex=True) # 특수문자 제거
       data2=data[[" Meter ID"," Received Time"," APT"," RPT"," PFT"," 검침구분"]]
       data2.rename(columns={' APT':'APT'},inplace=True) #이하 처리를 위한 행제목 변경
       data2.rename(columns={' RPT':'RPT'},inplace=True)	      
       data2.rename(columns={' PFT':'PFT'},inplace=True)	   
       data2.rename(columns={' Meter ID':'MeterID'},inplace=True)
       data2.rename(columns={' Received Time':'CTime'},inplace=True)          
       data2.rename(columns={' 검침구분':'sel'},inplace=True)  
		
       data2['APT']=pd.to_numeric(data2['APT'],errors='coerce')
       data2['RPT']=pd.to_numeric(data2['RPT'],errors='coerce')
       data2['PFT']=pd.to_numeric(data2['PFT'],errors='coerce')
	   
       data6=data2.drop_duplicates('MeterID',keep='first') # 미터정보만 남김
       data6.MeterID.count() #전체 미터 갯수
       data6.MeterID.values #전체 미터 번호
       data6=data6.reset_index(drop=True)
	   
       data7=data2[['CTime']] # 시간축 데이터만 잘라냄
       data7['CTime']=data7['CTime'].apply(lambda e:e.split()[0]) # 블록단위로 자름
       data7=data7.drop_duplicates('CTime',keep='first')
       data7.sort_values('CTime')
       data7=data7.reset_index(drop=True)
	   
       for i in range(0,data6.MeterID.count()):
        for j in range(0,data7.CTime.count()):
         data8=data2[(data2.MeterID==data6.MeterID[i])] # 아래의 경우 2*o로 사용가능
         data8=data8[(data8['CTime'].str.contains(data7.CTime[j]))]
         data9=data8[(data8['sel'].str.contains("현재검침"))]
         data8=data8[(data8['sel'].str.contains("정기검침"))]
         k=data8.APT.count() # 하루치 정기검침 갯수
         l=data9.APT.count() # 하루치 현재검침 갯수
		 
         if k!=0 and k!=6: #일일 LP 개수가 정상이 아닐경우 체크
          print(k,'개 입니다. 1')
          self.textBrowser.append('정기 검침')		  
          self.printall(1,data6.MeterID[i],data7.CTime[j],str(k))
         if not(94<l<97): #일일 LP 개수가 정상이 아닐경우 체크
          if k!=0:  
           self.textBrowser.append('현재 검침')				  
           self.printall(1,data6.MeterID[i],data7.CTime[j],str(l))
		   
         check=data8['APT'].isnull().sum()+data8['RPT'].isnull().sum()+data8['PFT'].isnull().sum()
         if check>0:
            self.printall(2,data6.MeterID[i],data7.CTime[j],str(k))
         else :
		   
          data10=data8[data8['APT']>10000000]
          data10=data10+data8[data8['APT']<0]
          data10=data10+data8[data8['RPT']>10000000]
          data10=data10+data8[data8['RPT']>10000000]
          data10=data10+data8[data8['PFT']>1]
          data10=data10+data8[data8['PFT']<-1]  

          data11=data9[data9['APT']>10000000]
          data11=data11+data9[data9['APT']<0]
          data11=data11+data9[data9['RPT']>10000000]
          data11=data11+data9[data9['RPT']>10000000]
          data11=data11+data9[data9['PFT']>1]
          data11=data11+data9[data9['PFT']<-1] 
		 
          if data10.empty==False: #하나라도 쓰레기값 범위인 경우
            self.textBrowser.append('정기 검침')				  
            self.printall(3,data6.MeterID[i],data7.CTime[j],str(k))   		 
          if data11.empty==False: #하나라도 쓰레기값 범위인 경우
            self.textBrowser.append('현재 검침')		
            self.printall(3,data6.MeterID[i],data7.CTime[j],str(k))    		 
		   
   def avg(self): #G,AE타입 평균전압/전류
       data=pd.read_csv(fname[0])
       data=data.replace(['"','='],['',''],regex=True) # 특수문자 제거
       if ' AVG_VOL' in data.columns :
        data2=data[[" Meter ID"," VOL CTime"," AVG_VOL"," AVG_AMP"]]
        data2.rename(columns={' AVG_VOL':'VOL'},inplace=True) #이하 처리를 위한 행제목 변경
        data2.rename(columns={' AVG_AMP':'AMP'},inplace=True)	      
        data2.rename(columns={' Meter ID':'MeterID'},inplace=True)
        data2.rename(columns={' VOL CTime':'CTime'},inplace=True)          

       elif ' VOL_AB' in data.columns :
        data2=data[[" Meter ID"," VOL CTime"," VOL_AB"," AMP_A"]]
        data2.rename(columns={' VOL_AB':'VOL'},inplace=True) #이하 처리를 위한 행제목 변경
        data2.rename(columns={' AMP_A':'AMP'},inplace=True)	      
        data2.rename(columns={' Meter ID':'MeterID'},inplace=True)
        data2.rename(columns={' VOL CTime':'CTime'},inplace=True)       
		
       else :
        self.textBrowser.append('파일이 이상합니다. 확인이 필요합니다.')		   
		
       data2['VOL']=pd.to_numeric(data2['VOL'],errors='coerce')
       data2['AMP']=pd.to_numeric(data2['AMP'],errors='coerce')

       data6=data2.drop_duplicates('MeterID',keep='first') # 미터정보만 남김
       data6.MeterID.count() #전체 미터 갯수
       data6.MeterID.values #전체 미터 번호
       data6=data6.reset_index(drop=True)
	   
       data7=data2[['CTime']] # 시간축 데이터만 잘라냄
       data7['CTime']=data7['CTime'].apply(lambda e:e.split()[0]) # 블록단위로 자름
       data7=data7.drop_duplicates('CTime',keep='first')
       data7.sort_values('CTime')
       data7=data7.reset_index(drop=True)
	   
       for i in range(0,data6.MeterID.count()):
        for j in range(0,data7.CTime.count()):
         data8=data2[(data2.MeterID==data6.MeterID[i])] # 아래의 경우 2*o로 사용가능
         data8=data8[(data8['CTime'].str.contains(data7.CTime[j]))]
         k=data8.VOL.count() # 하루치 평균전압전류 갯수
		 
         if k!=96: #일일 LP 개수가 정상이 아닐경우 체크
          if k!=0:  
            self.printall(1,data6.MeterID[i],data7.CTime[j],str(k))

         check=data8['VOL'].isnull().sum()+data8['AMP'].isnull().sum()
         if check>0:
            self.printall(2,data6.MeterID[i],data7.CTime[j],str(k))  
         else :		   
          data10=data8[data8['VOL']>235]
          data10=data10+data8[data8['VOL']<220]
          data10=data10+data8[data8['AMP']>10]
          data10=data10+data8[data8['AMP']<0] 

          if data10.empty==False: #하나라도 쓰레기값 범위인 경우
            self.printall(3,data6.MeterID[i],data7.CTime[j],str(k))		 	   
		   
   def btn_clicked(self):   #버튼 클릭시 동작사항을 추가, 들여쓰기에 주의할것
       global fname
       fname=QFileDialog.getOpenFileName(self)
       if meter==0:
        self.textBrowser.append("미터 종류를 선택해라") #미터 종류 미선택
       elif '.csv' in fname[0]:
	   #검침구분 추출
	   #self.glp()
        sw = True
        df=pd.read_csv(fname[0])
        df=df.replace(['"','='],['',''],regex=True)		   
        if meter!=3:
         if ' 검침구분' in df.columns :
          df2=df[[' 검침구분']]
          df2.rename(columns={' 검침구분':'sel'},inplace=True)
          df2=df2.drop_duplicates('sel',keep='first')
         else :
          sw = False # S타입으로 선택 했는데 S타입 데이터가 아닌경우
	  #self.srg()
		#미터타입과 검침구분 확인
        if meter==1 and sw:
         if df2.sel[0]=='순방향 LP' or df2.sel[0]=='순+역방향 LP':	#G,AE LP검침
          self.glp()
          self.textBrowser.append('G,AE타입 LP 판별 완료')    
         elif df2.sel[0]=='순방향 정기검침' or df2.sel[0]=='역방향 정기검침':	#G,AE 정기검침	
          self.grg()		 
          self.textBrowser.append('G,AE타입 정기검침 판별 완료')
         elif df2.sel[0]=='평균전압/전류':	#G,AE 평균전압/전류		
          self.avg()
          self.textBrowser.append('G,AE타입 평균전압/전류 판별 완료')		 
         else:
          	self.textBrowser.append('G,AE 타입 파일이 아닙니다.')		 
        elif meter==2 and sw:
         if df2.sel[0]=='LP': #E타입 LP
          self.elp()
          self.textBrowser.append('E타입 LP 판별 완료')			
         elif df2.sel[0]=='정기검침': #E타입 정기검침
          self.erg()
          self.textBrowser.append('E 타입 정기검침 판별 완료')
         else :
          	self.textBrowser.append('E타입 파일이 아닙니다.')
        elif meter==3:
         if ' 검침구분' in df.columns :
          df.rename(columns={' 검침구분':'sel'},inplace=True)
          if df.sel[0]=='현재검침' or df.sel[1]=='현재검침' or df.sel[2]=='현재검침':
           self.srg()
           self.textBrowser.append('S타입 정기/현재검침 판별 완료')			   
          else :
           self.textBrowser.append('S 타입 파일이 아닙니다.')
         elif ' FAP' in df.columns :
          self.glp()
          self.textBrowser.append('S타입 LP 판별 완료')	
         else :
          self.textBrowser.append('파일을 확인해주세요')
          #self.glp()		
    #      self.srg()			  
   #      elif df2.sel[0]=='정기검침' or '현재검침': #S타입 정기검침
   #       
       else:
        self.textBrowser.append('csv파일이 아닙니다.') #csv파일이 아닐시		   
       #self.textBrowser.append(fname[0]) #테스트용 구문	   
       #self.textBrowser.append(str(meter)) #테스트용 구문

   def btn2_clicked(self):	 
       self.textBrowser.clear()
       self.textBrowser_2.clear()
	   
if __name__ == "__main__":
   app = QApplication(sys.argv)
   myWindow = MyWindow()
   myWindow.show()
   app.exec_()
