<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>
 24 hour Time Stats
    </title>
	<meta http-equiv="refresh" content="300">
	<meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-1">
  </head>
  <body bgcolor="c8d5e6">
	<basefont face="Ariel">

<center>
<h2> YaDDNet : MF/HF DSC Database</h2>

<h3>This view is of</h3>
24 hour Ship Station Message count (with OK Checksum)
<br><br>
<?php
$freq=$_GET['rx_freq'];


$timescale = $_GET['timescale'];

echo "Showing last : " . $timescale . " days<br><br>";




$order=$_GET['order'];

if ($order=="Name")
{
$order_by = "FROM_NAME";
}
else if ($order == "Country")
{
$order_by = "FROM_CTRY";
}
else
{
$order_by = "RAW_FROM_MMSI";
}

echo "<br><br>";
echo "Sorted by  : ";
echo $order;
echo "<br><br>";



if ($freq=="All")
{
$rx_freq="%";
}
else 
{
$rx_freq=$freq;
}

//echo $rx_freq;

$fd=exec("date +%Y-%m-%d-%H%M%S");

$file='./test/tmp/' . $fd . '.txt';

$f = fopen($file, 'w');
$header = "Frequency = $freq\r\n\n======================================================\r\nMsg\tRX\tMMSI\t\tShip Station\r\n\n";
fwrite($f, $header);


$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno())
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
echo "Text file output for copying into documents/email etc <br>";      
        echo "Click to read or 'Right Click' to Save As...<a href=".$file.">File output</a>  :<br><br>";



$result = mysqli_query($con,"select count(distinct RAW_FROM_MMSI) from newlog where datetime > date_sub(utc_timestamp(), interval ".$timescale." day) and rx_freq like '".$rx_freq."%' and FROM_TYPE = 'SHIP' and RAW_FROM_MMSI not like '%~%'  and FROM_NAME not like '%UNID%' and ECC not like '%ERR%'");

echo "<table border='0' cellpadding='2' rules='rows'>
<tr>
<th><font face=monospace color=#424242 size='3pt'>Ship Stations<br>" . $freq . "</font></th>
</tr>";

while($row = mysqli_fetch_array($result))
 {
 
  echo "<td nowrap align='center'><font  face=monospace color=#424242 size='3pt'>" . $row['count(distinct RAW_FROM_MMSI)'] . "</font></td>";
  
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

$result = mysqli_query($con,"select RAW_FROM_MMSI, FROM_NAME, FROM_CTRY, count(*), count(distinct rx_id), count(distinct rx_freq) from newlog where datetime > date_sub(utc_timestamp(), interval ".$timescale." day) and rx_freq like '%".$rx_freq."%' and FROM_TYPE = 'SHIP'  group by RAW_FROM_MMSI order by ".$order_by." asc");



echo "<table border='0' cellpadding='5' rules='all'>
<tr>

<th><font face=monospace color=#424242 size='3pt'>MMSI</font></th>
<th><font face=monospace color=#424242 size='3pt'>Name</font></th>
<th><font face=monospace color=#424242 size='3pt'>Country</font></th>
<th><font face=monospace color=#424242 size='3pt'>24 Hour<br>Messages<br>" . $freq . "</font></th>
<th><font face=monospace color=#424242 size='3pt'>Freqs</font></th>
<th><font face=monospace color=#424242 size='3pt'>Reporters</font></th>

</tr>";
$i=0;
while($row = mysqli_fetch_array($result)) {

  echo "<td nowrap ><font face=monospace color='blue' size='3pt'><a href='./band_ship_search.php?from_mmsi=" . $row['RAW_FROM_MMSI'] . "&rx_freq=" . $rx_freq ."'>" . $row['RAW_FROM_MMSI'] . "</a></font></td>";


  echo "<td nowrap><font  face=monospace color=#424242 size='3pt'>" . $row['FROM_NAME'] . "</font></td>";
  echo "<td nowrap><font  face=monospace color=#424242 size='3pt'>" . $row['FROM_CTRY'] . "</font></td>";
  echo "<td nowrap align='center'><font  face=monospace color=#424242 size='3pt'>" . $row['count(*)'] . "</font></td>";
  echo "<td nowrap align='center'><font  face=monospace color=#424242 size='3pt'>" . $row['count(distinct rx_freq)'] . "</font></td>";
    echo "<td nowrap align='center'><font  face=monospace color=#424242 size='3pt'>" . $row['count(distinct rx_id)'] . "</font></td>";
  
  echo "</tr>";
  $i++;
  $from_mmsi = $row['RAW_FROM_MMSI'];
  $from_name = $row['FROM_NAME'];
  $from_ctry = $row['FROM_CTRY'];
  $count = $row['count(*)'];
  $count_rx = $row['count(distinct rx_id)'];
  $count_freq = $row['count(distinct rx_freq)'];
  
  $output = "$count\t$count_rx\t$from_mmsi\t$from_name, $from_ctry\r\n";
  
  fwrite($f, $output);
  }
 
echo "</table>";
echo "<font  face=monospace color=#424242 size='3pt'>";
 echo "Total : " . $i . "<br>";
echo "</font>";

fwrite($f, "\n\r=====================================================\n\rTotal Ship Stations: $i");

mysqli_close($con);


fclose($f);
?>
</td>


</tr>
</table>


</center>
<center><br><a href="../../index.php">HOME</a>
</body>
</html>




