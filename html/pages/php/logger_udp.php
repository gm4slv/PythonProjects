<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>
Logger
    </title>
	<meta http-equiv="refresh" content="120">
  </head>
  <body bgcolor="c8d5e6">
	<basefont face="Ariel">

<center>
<h2> YaDDNet : MF/HF DSC Database</h2>

<h3>This view is of</h3>
<b>System Log</b>: Incoming message server activity - last 3 hours
<br>
<br>


<?php



$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
 
$result = mysqli_query($con,"select * from logger where id = 'UDP' and datetime > date_sub(utc_timestamp(), interval 180 minute) order by P_Id desc;");


echo "<table border='0' cellpadding='4' rules='all'>
<tr>

<th><font face=monospace color=blue size='4pt'>Date/Time</font></th>

<th><font face=monospace color=black size='4pt'>ID</font></th>
<th align=left><font face=monospace color=green size='4pt'>Message</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
 {
  echo "<td nowrap><font  face=monospace color=blue size='3pt'>" . $row['DATETIME'] . "</font></td>";
 
  echo "<td nowrap><font  face=monospace color=black size='3pt'>" . $row['ID'] . "</font></td>";
echo "<td nowrap><font  face=monospace color=green size='3pt'>" . $row['MESSAGE'] . "</font></td>";		
  
  echo "</tr>";
  }
echo "</table>";
echo "</font>";

mysqli_close($con);
?>


</center>
<center><br><a href="../../index.php">HOME</a></body>
</html>

