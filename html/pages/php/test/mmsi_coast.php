<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>
Coast Station Names
    </title>
	<meta http-equiv="refresh" content="300">
  </head>
  <body bgcolor="9AB3DA">
	<basefont face="Ariel">

<center>
<h2> GM4SLV : MF/HF DSC Database</h2>

<h3>This view is of</h3>
<b>MMSI to Coast Station resolution database</b>
<br>

<?php






$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"SELECT count(*) FROM coast");


echo "<table border='0' cellpadding='3' rules='all'>
<tr>



<th> <font  face=monospace color=blue size='3pt'>Coast Stations Known</font></th>

</tr>";

while($row = mysqli_fetch_array($result))
  {
    echo "<tr>";

  echo "<td align=center><font face=monospace color=blue size='3pt'>"  . $row['count(*)'] . "</font> </td>";


  echo "</tr>";
  }
echo "</table>";
echo "</font>";

mysqli_close($con);
?>




<?php

$fd=exec("date +%Y-%m-%d-%H%M%S");

$file='./tmp/yadd_mmsi_coast_' . $fd . '.txt';

$f = fopen($file, 'w');

$date=exec("date +%Y%m%d");
$header="Version = V6.0\r\nDate= $date\r\nEditor=John Pumford-Green (YaDDNet)\r\n";

fwrite($f, $header);

$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"SELECT * FROM coast");
echo "<h3>File Downloads</h3>";
echo "Text file in <b><i>yadd_mmsi_coast.txt</b></i> format suitable for use in <b>YaDD 1.7</b><br>";      
echo "Click to read or 'Right Click' to Save As...<a href=".$file.">File output</a>  :<br><br>";


echo "<table border='0' cellpadding='6' rules='all'>
<tr>



<th> <font  face=monospace color=black size='3pt'>MMSI</font></th>
<th> <font  face=monospace color=blue size='3pt'>MID</font></th>
<th> <font  face=monospace color=black size='3pt'>Coast Station</font></th>
<th><font face=monospace color=black size='3pt'>CCC</font></th>
<th><font face=monospace color=black size='3pt'>Ctry</font></th>
<th><font face=monospace color=black size='3pt'>Lat</font></th>
<th><font face=monospace color=black size='3pt'>Lon</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
  {
    echo "<tr>";

  echo "<td ><font face=monospace color=black size='3pt'>"  . $row['MMSI'] . "</font> </td>";
  echo "<td><font face=monospace color=blue size='3pt'>" . $row['MID'] . "</font></td>";
  echo "<td><font face=monospace color=black size='3pt'>"  . $row['COASTNAME'] . "</font> </td>";
  echo "<td><font face=monospace color=black size='3pt'>"  . $row['CCC'] . "</font> </td>";
  echo "<td><font face=monospace color=black size='3pt'>"  . $row['CTRY'] . "</font> </td>";
  echo "<td><font face=monospace color=black size='3pt'>"  . $row['LAT'] . "</font> </td>";
  echo "<td><font face=monospace color=black size='3pt'>"  . $row['LON'] . "</font> </td>";

  echo "</tr>";
  
  $mmsi = $row['MMSI'];
  $ccc = $row['CCC'];
  $coastname = $row['COASTNAME'];
  $lat = $row['LAT'];
  $lon = $row['LON'];
  $output = "$mmsi,$ccc,$coastname,$lat,$lon\r\n";
  fwrite($f, $output);
  }
echo "</table>";
echo "</font>";
fclose($f);
mysqli_close($con);
?>
</center>
<center><br><a href="../../index.html">HOME</a></body>
</html>

