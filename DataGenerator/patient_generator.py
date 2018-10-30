#!/usr/bin/env python
# coding: utf-8

# In[1]:


from species_generator import generate_species,search_species,convert_format
from name_generator import generate_names,convert_name,standard_formats
import pandas as pd
import random


# In[2]:


frame_columns = ["PatientName","Attendings","IPCStaff","Pathogen"] 

patient_info = pd.DataFrame(columns=frame_columns) #init a blank table
num_patients = 100 
patient_names = generate_names(100,"f l") #create the set of patient names
attendings_names = generate_names(30,"f m l") #attending full names
ipc_names = generate_names(20,"f m l") #ipc member full names

for patient in patient_names:
    patient = convert_name(patient,"f l",'l, f')
    #pick a random attending and random name format
    curr_attending = convert_name(random.choice(attendings_names),"f m l","mix")
    #do the same for a random number of staff
    curr_staff = random.choices(ipc_names,k=random.randint(1,5))
    for i in range(len(curr_staff)):
        curr_staff[i] = convert_name(curr_staff[i],"f m l","mix")
    curr_staff = ";".join(curr_staff)
    #generate a random pathogen
    curr_pathogen = ";".join(generate_species(random.randint(1,3),bool(random.randint(1,1))))
    #append row to data frame
    row = [patient,curr_attending,curr_staff,curr_pathogen]
    patient_info = patient_info.append(pd.DataFrame([row],columns=frame_columns),ignore_index = True)


# In[14]:


patient_info
patient_name_df = pd.DataFrame(columns=["PatientName"])
patient_name_df["PatientName"] = patient_names
attending_name_df = pd.DataFrame(columns=["AttendingName"])
attending_name_df["AttendingName"] = attendings_names
ipc_name_df = pd.DataFrame(columns=["IPCStaffName"])
ipc_name_df["IPCStaffName"] = ipc_names


# In[18]:


patientWriter = pd.ExcelWriter('sample_patients.xlsx')
patientNameWriter = pd.ExcelWriter('sample_patient_names.xlsx')
ipcWriter = pd.ExcelWriter('sample_ipc.xlsx')
attendingWriter = pd.ExcelWriter('sample_attendings.xlsx')
patient_info.to_excel(patientWriter,'Sheet1',index=False)
patient_name_df.to_excel(patientNameWriter,'Sheet1',index=False)
attending_name_df.to_excel(attendingWriter,'Sheet1',index=False)
ipc_name_df.to_excel(ipcWriter,'Sheet1',index=False)
patientWriter.close()
patientNameWriter.close()
ipcWriter.close()
attendingWriter.close()


# In[ ]:




