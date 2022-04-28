<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Search</title>
    <meta http-equiv="Content-Type" content="text/html" />
<style>

 #freq{
color: #424242;
background: #006666;
width:60px;
height:30px;
border-radius: 10px
}
 #rx {
color: #424242;
background: #6666cc;
width:140px;
height:30px;
border-radius: 10px
}
#link {
color: #424242;
background: #6699cc;
width:140px;
height:30px;
border-radius: 10px;
font-weight: bold;
}
#dis {
color: #b0b0b0;
background: #d0d0d0;
width:140px;
height:30px;
border-radius: 10px
}
input[type=submit]{
color: #424242;
background: #003366;
width:60px;
height:30px;
border-radius: 10px
font-weight: bold;
}
select {
color: #424242;
background: #6699cc;
border-radius: 10px;
height: 30px;

font-weight: bold;
}
input[type=text]{
color: #424242;
background: #cccccc;
width:140px;
height:30px;
border-radius: 10px;
border-width: 1px;
font-family: monospace;
font-size: 15px;
font-weight: bold;
padding-left: 10px;
}

 

</style>
</head>
<body bgcolor="c8d5e6">
        <basefont face="Arial">
<center>
<h3>DSC Messages from specific Receivers</h3>
Previous 24 hours.
    <form action="./search_rx.php" method="GET">
<table cellpadding="5">

<tr>
<td><center><input type="text" name="rxid" /><br><font color=#424242 size="2pt"></center></td>
</tr>
<tr>
<td><center>Enter a full or partial RXID string</font></center></td>
</tr>
</table>
<hr width=50%>
<input id="link" type="submit" value="Search" />
<br>
<hr width=50%>
<input id="link" type="reset" value="Reset" />
</form>


</center>
<center><br><a href="../../index.php">HOME</a></body>
</html>
