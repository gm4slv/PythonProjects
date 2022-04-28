<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Search</title>
    <meta http-equiv="Content-Type" content="text/html" />
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>

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
<h3>DSC Conversation search</h3>

<table cellpadding=10 rules=all>


<tr>
<td>
<center>
Coast MMSI<br> 
Last 50 messages between ONE Coast and ALL ships<br>
Test Calls excluded<br>
<form action="./search_qso2.php" method="GET">
<input type="text" name="coast_mmsi">
<input id="link" type="submit" value="MMSI" />
</form>
</center>
</td>



<td>
<center>
Coast MID<br>
Last 50 messages bewteen ALL Coast stations with<br>
the Selected MID and ALL ships<br>
Test Calls excluded<br>
<form action="./search_qso_mid.php" method="GET">
<input type="text" name="coast_mid">
<input id="link" type="submit" value="MID" />
</form>
</center>
</td>


<td>
<center>
Coast MMSI<br>
All stored messages between ONE coast station and ALL ships<br>
Test Calls excluded<br>
Only csv file output<br>
<form action="./search_qso_dump.php" method="GET">
<input type="text" name="coast_mmsi">
<input id="link" type="submit" value="MMSI" />
</form>
</center>
</td>


</tr>
<tr>
<td>
<center>
MMSI / MMSI<br>
Last 50 messages between any TWO selected MMSI (Coast or Ship)<br>
Test Calls included<br>
<form action="./search_qso.php" method="GET">
<input type="text" name="coast_mmsi"> MMSI<br>
<input type="text" name="ship_mmsi"> MMSI<br>
<input id="link" type="submit" value="MMSI MMSI" />
</form>
</center>
</td>

<td>
<center>
MMSI / MMSI<br>
Last 50 messages between any TWO selected MMSI (Coast or Ship)<br>
Test Calls excluded<br>
<form action="./search_qso_3.php" method="GET">
<input type="text" name="coast_mmsi"> MMSI<br>
<input type="text" name="ship_mmsi"> MMSI<br>
<input id="link" type="submit" value="MMSI MMSI" />
</form>
</center>
</td>

</table>

<center><br><a href="../../../../index.php">BACK</a></body>
</html>
