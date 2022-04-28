<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>
UNIDS</title>
	<meta http-equiv="refresh" content="600">
	<meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-1">
  </head>
  <body bgcolor="c8d5e6">
	<basefont face="Ariel">

<center>
<h2> YaDDNet : MF/HF DSC Database</h2>

<h3>This view is of</h3>
Unidentified Coast Stations reported in the last 30 days.<br><br>
Listed in order of number of messages seen from the UNID Station.<br><br>
You can click the MMSI to search for all messages to or from the UNID Coast Station.
<br><br>
<?php



$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"select DATETIME, RX_FREQ, RX_ID, MIN(RAW_FROM_MMSI), FROM_MID, FROM_CTRY, count(distinct rx_id), count(distinct rx_freq),count(*) from newlog where datetime > date_sub(utc_timestamp(), interval 30 day) and  ecc not like '%err%' and FROM_TYPE='COAST' and FROM_NAME like '%unid%' and RAW_FROM_MMSI not like '%~%' group by raw_from_mmsi order by count(*) desc");  


echo "<table border='0' cellpadding='5' rules='all'>
<tr>
<th> <font face=monospace color=blue size='3pt'>First Reported<br>Date  /  UTC</font></th>
<th> <font face=monospace color=blue size='3pt'>First Reported<br>Frequency</font></th>
<th> <font face=monospace color=blue size='3pt'>First Reported<br>by RX_ID</font></th>

<th> <font  face=monospace color=DarkGreen size='3pt'>Unid Coast Station</font></th>
<th><font face=monospace color=#541b66 size='3pt'>MID</font></th>
<th><font face=monospace color=#541b66 size='3pt'>Country</font></th>
<th><font face=monospace color=blue size='3pt'>Number of<br>Messages</font></th>
<th><font face=monospace color=#424242 size='3pt'>Number of<br>Reporters</font></th>
<th><font face=monospace color=#424242 size='3pt'>Number of<br>Frequ.</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
  {
    echo "<tr>";
  echo "<td><font face=monospace color=blue size='3pt'>"  . $row['DATETIME'] . "</font> </td>";
  echo "<td> <center><font face=monospace color=blue size='3pt'>"  . $row['RX_FREQ'] . "</font> </td>";
  echo "<td><font face=monospace color=blue size='3pt'>"  . $row['RX_ID'] . "</font> </td>";
  
echo "<td nowrap ><font face=monospace color='blue' size='3pt'><a href='./unid_search.php?from_mmsi=" . $row['MIN(RAW_FROM_MMSI)'] . "'>" . $row['MIN(RAW_FROM_MMSI)'] . "</a></font></td>"; 
  
  echo "<td><font  face=monospace color=#541b66 size='3pt'>" . $row['FROM_MID'] . "</font></td>";
  echo "<td><font  face=monospace color=#541b66 size='3pt'>" . $row['FROM_CTRY'] . "</font></td>";
  echo "<td><font  face=monospace color=blue size='3pt'>" . $row['count(*)'] . "</font></td>";
  echo "<td><font  face=monospace color=#424242 size='3pt'>" . $row['count(distinct rx_id)'] . "</font></td>";
  echo "<td><font  face=monospace color=#424242 size='3pt'>" . $row['count(distinct rx_freq)'] . "</font></td>";
  echo "</tr>";
  }
echo "</table>";
echo "</font>";

mysqli_close($con);
?>
</center>
<center><br><a href="../../index.php">HOME</a></body>
</html>

