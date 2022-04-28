<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>
Ship Names
    </title>
	<meta http-equiv="refresh" content="300">
  </head>
  <body bgcolor="9AB3DA">
	<basefont face="Ariel">

<center>
<h2> GM4SLV : MF/HF DSC Database</h2>

<h3>This view is of</h3>
<b>MMSI to Shipname resolution database</b>
<br>
Listed with latest addition first
<br>

<?php






$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"SELECT count(*) FROM resolve2");


echo "<table border='0' cellpadding='3' rules='all'>
<tr>



<th> <font  face=monospace color=blue size='3pt'>Ships Known</font></th>

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

<br>
<br>


<?php

$fd=exec("date +%Y-%m-%d-%H%M%S");

$file='./test/tmp/' . $fd . '.txt';

$f = fopen($file, 'w');


$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"SELECT * FROM resolve2 order by p_id desc");

echo "Text file in \";\" delimited format for import into Excel etc.<br>";      
echo "Click to read or 'Right Click' to Save As...<a href=".$file.">File output</a>  :<br><br>";
echo "For other formats (YaDD/DSCDecoder) use the \"Ordered\" listing <a href=\"./mmsi_shipname_ordered.php\"> HERE</a><br><br>";
echo "<table border='0' cellpadding='4' rules='all'>
<tr>



<th> <font  face=monospace color=black size='3pt'>MMSI</font></th>
<th> <font  face=monospace color=blue size='3pt'>Ship Name</font></th>
<th> <font  face=monospace color=black size='3pt'>Callsign</font></th>
<th><font face=monospace color=black size='3pt'>Vessel Type</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
  {
    echo "<tr>";

  echo "<td width=20%><font face=monospace color=black size='3pt'>"  . $row['MMSI'] . "</font> </td>";
  echo "<td width=40%><font face=monospace color=blue size='3pt'>" . $row['SHIPNAME'] . "</font></td>";
  echo "<td width=20%><font face=monospace color=black size='3pt'>"  . $row['CALLSIGN'] . "</font> </td>";
  echo "<td width=20%><font face=monospace color=black size='3pt'>"  . $row['VESSELTYPE'] . "</font> </td>";

  echo "</tr>";
  
  $mmsi = $row['MMSI'];
  
  $shipname = $row['SHIPNAME'];
  $callsign = $row['CALLSIGN'];
  $vesseltype = $row['VESSELTYPE'];
  
  $output = "$mmsi;$shipname;$callsign;$vesseltype\r\n";
  
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

