<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<title>LanSite</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<link rel="stylesheet" href="base.css" type="text/css" />
</head>
<body>
<center>
	<h1> LanSite </h1>
	<table width="100%" border="0"> <tr align="center" bgcolor="lightgrey">
		<!--td> <a href="insupol"> InsuPol </a> </td-->
		<!--td> <a href="run1s"> Run1s </a> </td-->
		<!--td> <a href="sro"> СРО </a> </td-->
		<td> <a href="{% url sro2.views.index %}"> СРО2 </a> </td>
		<td> <a href="{% url todo.views.index %}"> ToDo </a> </td>
		<td> <a href="admin"> Администрирование </a> </td>
	</tr> </table>
</center>

<p> Пользователь: {% if user.is_authenticated %} {{ user.username }} (<a href="logout/"> Logout </a>) {% else %} anonymous {% endif %} </p>
</body>
</html>