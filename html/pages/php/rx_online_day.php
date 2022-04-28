<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>
 Online Receivers
    </title>
	<meta http-equiv="refresh" content="300">
  </head>
  <body bgcolor="c8d5e6">
	<basefont face="Ariel">

<center>
<h2>Active receivers today and their frequencies</h2>
<h3>Previous 24 Hours</h3>
<table cellpadding=20>
<tr>
<td>


<?php
$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }


$result = mysqli_query($con,"select distinct RX_ID, RX_FREQ from newlog where datetime > date_sub(utc_timestamp(), interval 24 hour) order by RX_ID, abs(RX_FREQ)");

echo "<table border='0' cellpadding='5' rules='all'>
<tr>

<th><font face=monospace color=black size='3pt'>RX_ID</font></th>
<th><font face=monospace color=black size='3pt'>RX Freq</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
 {

echo "<td nowrap ><font face=monospace color='blue' size='3pt'><a href='./search_rx_freq.php?rxid=" . $row['RX_ID'] . "&rx_freq=" . $row['RX_FREQ']."'>" . $row['RX_ID'] . "</a></font></td>";
//  echo "<td nowrap ><font face=monospace color='blue' size='3pt'>" . $row['RX_ID'] . "</font></td>";
  echo "<td nowrap align='center'><font  face=monospace color='blue' size='3pt'>" . $row['RX_FREQ'] . "</font></td>";
  
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


$result = mysqli_query($con,"select distinct RX_ID, RX_FREQ from newlog where datetime > date_sub(utc_timestamp(), interval 24 hour) order by abs(RX_FREQ), RX_ID");

echo "<table border='0' cellpadding='5' rules='all'>
<tr>
<th><font face=monospace color=black size='3pt'>RX Freq</font></th>

<th><font face=monospace color=black size='3pt'>RX_ID</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
 {


  echo "<td nowrap align='center'><font  face=monospace color='blue' size='3pt'>" . $row['RX_FREQ'] . "</font></td>";
//  echo "<td nowrap ><font face=monospace color='blue' size='3pt'>" . $row['RX_ID'] . "</font></td>";
echo "<td nowrap ><font face=monospace color='blue' size='3pt'><a href='./search_rx_freq.php?rxid=" . $row['RX_ID'] . "&rx_freq=" . $row['RX_FREQ']."'>" . $row['RX_ID'] . "</a></font></td>";
  
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
</body>
</html>
