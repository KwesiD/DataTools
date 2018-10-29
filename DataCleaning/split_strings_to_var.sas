/*referenced from 
https://communities.sas.com/t5/SAS-Programming/adding-a-row-by-using-DATA-step/td-p/38221
and 
https://communities.sas.com/t5/General-SAS-Programming/Splitting-String-that-contains-commas/td-p/344645
*/
data employee_departments; /*new dataset*/
set employees;  /*old dataset*/
keep Employee Departments; /*we want to split the departments and have a name attached to each*/
temp = Departments; /*temp variable for some reason*/
do i = 1 to countw(temp,';');
	dept = scan(temp,i,';'); /*new column dept has the split departments*/
	output;
end;
keep dept;
drop Departments; /*drop old department var. Employee names are now double counted for multiple departments*/
run;

proc sgplot data=employee_departments;
VBAR dept;
run;

