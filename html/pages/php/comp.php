<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>
 RX Stats
    </title>
	<meta http-equiv="refresh" content="300">
  </head>
  <body bgcolor="c8d5e6">
	<basefont face="Ariel">

<center>
<h2> GM4SLV : MF/HF DSC Database</h2>

<h3>This view is of</h3>
Message Rate<br>
Only messages with "Checksum Correct / ECC=OK" are included in the count.<br>
<br>
<?php
$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"select count(*) from newlog where  datetime>date_sub(utc_timestamp(), interval 60 minute)  and ecc = 'OK' ");


echo "<table border='0' cellpadding='10' rules='rows'>

<tr>


<th><font face=monospace color=blue size='3pt'>Total Messages<br>From All Receivers<br>Last 60 minutes</font></th>

</tr>";
while($row = mysqli_fetch_array($result))
 {

  echo "<td nowrap align='center'><font  face=monospace color=blue size='3pt'>" . $row['count(*)'] . "</font></td>";

  echo "</tr>";
  }
echo "</table>";
echo "</font>";
?>
<table border=0 cellpadding=10 rules=all>
<tr>
<td>
<?php
$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"select rx_id, rx_freq, count(*) from newlog where  datetime>date_sub(utc_timestamp(), interval 60 minute)  and ecc = 'OK' group by rx_id, rx_freq order by 3 desc");


echo "<table border='0' cellpadding='5' rules='rows'>

<tr>

<th><font face=monospace color=blue size='3pt'>RX</font></th>
<th><font face=monospace color=blue size='3pt'>Freq</font></th>
<th><font face=monospace color=blue size='3pt'>Total Messages<br>Last 60 minutes</font></th>

</tr>";
while($row = mysqli_fetch_array($result))
 {
echo "<td nowrap ><font face=monospace color='blue' size='3pt'><a href='./search_rx_freq.php?rxid=" . $row['rx_id'] . "&rx_freq=" . $row['rx_freq']."'>" . $row['rx_id'] . "</a></font></td>";

//  echo "<td nowrap><font  face=monospace color=blue size='3pt'>" . $row['rx_id'] . "</font></td>";
  echo "<td nowrap><font  face=monospace color=blue size='3pt'>" . $row['rx_freq'] . "</font></td>";
  echo "<td nowrap align='center'><font  face=monospace color=blue size='3pt'>" . $row['count(*)'] . "</font></td>";
 
  echo "</tr>";
  }
echo "</table>";
echo "</font>";
?>
<br>
<br>
<?php
$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"select rx_id, rx_freq, count(*), count(distinct raw_from_mmsi) from newlog where  datetime>date_sub(utc_timestamp(), interval 60 minute)  and ecc = 'OK' and FROM_TYPE = 'COAST' group by rx_id, rx_freq order by 3 desc");


echo "<table border='0' cellpadding='5' rules='rows'>

<tr>

<th><font face=monospace color=blue size='3pt'>RX</font></th>
<th><font face=monospace color=blue size='3pt'>Freq</font></th>
<th><font face=monospace color=blue size='3pt'>Total Messages<br>From Coast Stations<br>Last 60 minutes</font></th>
<th><font face=monospace color=blue size='3pt'>Unique Coast Stations<br>Last 60 minutes</font></th>
</tr>";
while($row = mysqli_fetch_array($result))
 {

echo "<td nowrap ><font face=monospace color='blue' size='3pt'><a href='./search_rx_freq.php?rxid=" . $row['rx_id'] . "&rx_freq=" . $row['rx_freq']."'>" . $row['rx_id'] . "</a></font></td>";

//  echo "<td nowrap><font  face=monospace color=blue size='3pt'>" . $row['rx_id'] . "</font></td>";
  echo "<td nowrap><font  face=monospace color=blue size='3pt'>" . $row['rx_freq'] . "</font></td>";
  echo "<td nowrap align='center'><font  face=monospace color=blue size='3pt'>" . $row['count(*)'] . "</font></td>";
    echo "<td nowrap align='center'><font  face=monospace color=blue size='3pt'>" . $row['count(distinct raw_from_mmsi)'] . "</font></td>";
  echo "</tr>";
  }
echo "</table>";
echo "</font>";
?>
<?php
mysqli_close($con);
?>
</td>
</tr>
</table>


<br><br>
</center>
<center><br><a href="../../index.php">HOME</a>
</body>
</html>

