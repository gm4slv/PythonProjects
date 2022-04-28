<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>
Live</title>
	<meta http-equiv="refresh" content="30">
  </head>
  <body bgcolor="c8d5e6">
	<basefont face="Ariel">

<center>
<h2> YaDDNet : MF/HF DSC Database</h2>

<h3>This view is of</h3>
<b>All</b> Messages, last 60 minutes : All connected YaDD monitors : All bands<br>
<br>
<br>
<br>

<?php


 

$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"SELECT * FROM newlog where datetime > date_sub(utc_timestamp(), interval 60 minute) order by datetime desc");


echo "<table border='0' cellpadding='5' rules='all'>
<tr>
<th> <font face=monospace color=blue size='3pt'>Date  /  UTC</font></th>
<th> <font  face=monospace color=crimson size='3pt'>Raw Message</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
  {
    echo "<tr>";
  echo "<td width='6%' nowrap><font face=monospace color=blue size='3pt'>"  . $row['DATETIME'] . "</font> </td>";
  echo "<td width='8%' nowrap><font  face=monospace color=#541b66 size='3pt'>" . $row['RAW_DSC_MESSAGE'] . "</font></td>";
  echo "</tr>";  }
echo "</table>";
echo "</font>";

mysqli_close($con);
?>
</center>
<center><br><a href="../../index.php">HOME</a></body>
</html>

