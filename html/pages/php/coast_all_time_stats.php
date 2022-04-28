<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>
 All Time Stats
    </title>
	<meta http-equiv="refresh" content="300">
  </head>
  <body bgcolor="c8d5e6">
	<basefont face="Ariel">

<center>
<h2> YaDDNet : MF/HF DSC Database</h2>

<h3>This view is of</h3>
All Time Coast Station Message count (with OK Checksum)
<br>
<br>
<?php
$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"select count(distinct FROM_MMSI) from log where FROM_MMSI like '%COAST%' and FROM_MMSI not like '%~%' and FROM_MMSI not like '%000000000%' and FROM_MMSI not like '%UNID%' and ECC not like '%ERR%'");


echo "<table border='0' cellpadding='2' rules='rows'>
<tr>
<th><font face=monospace color=#424242 size='3pt'>Unique Coast Stations<br>All Bands</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
 {
 
  echo "<td nowrap align='center'><font  face=monospace color=#424242 size='3pt'>" . $row['count(distinct FROM_MMSI)'] . "</font></td>";
  
  echo "</tr>";
  }
echo "</table>";
echo "</font>";

mysqli_close($con);
?>
<table border=0 cellpadding=10 rules="cols">
<tr>
<td>
<?php
$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"select FROM_MMSI, count(*) from log where FROM_MMSI like '%COAST%' and FROM_MMSI not like '%UNID%' and FROM_MMSI not like '%~%' and EOS not like '%~%' and ECC not like '%ERR%'  group by FROM_MMSI order by 1 asc");


echo "<table border='0' cellpadding='2' rules='rows'>
<tr>

<th><font face=monospace color=#424242 size='3pt'>By MMSI</font></th>
<th><font face=monospace color=#424242 size='3pt'>All Time<br>Messages</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
 {
  echo "<td nowrap><font  face=monospace color=#424242 size='3pt'>" . $row['FROM_MMSI'] . "</font></td>";
  echo "<td nowrap align='center'><font  face=monospace color=#424242 size='3pt'>" . $row['count(*)'] . "</font></td>";
  
  echo "</tr>";
  }
echo "</table>";
echo "</font>";

mysqli_close($con);
?>
</td>
<td>
<?php
$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"select FROM_MMSI, count(*) from log where FROM_MMSI like '%COAST%' and FROM_MMSI not like '%UNID%' and FROM_MMSI not like '%~%' and EOS not like '%~%' and ECC not like '%ERR%'  group by FROM_MMSI order by 2 desc");


echo "<table border='0' cellpadding='2' rules='rows'>
<tr>

<th><font face=monospace color=#424242 size='3pt'>By Message Count</font></th>
<th><font face=monospace color=#424242 size='3pt'>All Time<br>Messages</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
 {
  echo "<td nowrap><font  face=monospace color=#424242 size='3pt'>" . $row['FROM_MMSI'] . "</font></td>";
  echo "<td nowrap align='center'><font  face=monospace color=#424242 size='3pt'>" . $row['count(*)'] . "</font></td>";
  
  echo "</tr>";
  }
echo "</table>";
echo "</font>";

mysqli_close($con);
?>
</td>
</tr>
</table>


</center>
<center><br><a href="../../index.php">HOME</a></body>
</html>

