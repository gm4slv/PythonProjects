 
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Ship Stations vs Frequency</title>
    <meta http-equiv="Content-Type" content="text/html" />
</head>
 <body bgcolor="c8d5e6">
	<basefont face="Arial">
<center>

<h2> YaDDNet : MF/HF DSC Database</h2>

<h3>This view is of</h3>
Ship Stations per MID : 24 hours : All connected YaDD monitors :  Frequencies logged and number of messages on each frequency
<br>
<br>


<?php
  
$order=$_GET['order'];


$timescale = $_GET['timescale'];

echo "Showing last : " . $timescale . " days<br><br>";




if ($order=="Name")
{
$order_by = "from_name";
}
else if ($order == "Country")
{
$order_by = "from_ctry";
}
else
{
$order_by = "raw_from_mmsi";
}

//echo $order_by;
echo "Sorted by  : ";
echo $order;
echo "<br>";

//echo $order;
//echo "<br>";
//echo $order_by;

$mid1=$_GET['mid1'];

if ($mid1=="[200]")
{
$mid_min=200;
$mid_max=299;
}

if ($mid1=="[300]")
{
$mid_min=300;
$mid_max=399;
}

if ($mid1=="[400]")
{
$mid_min=400;
$mid_max=499;
}

if ($mid1=="[500]")
{
$mid_min=500;
$mid_max=599;
}

if ($mid1=="[600]")
{
$mid_min=600;
$mid_max=699;
}

if ($mid1=="[700]")
{
$mid_min=700;
$mid_max=799;
}
if ($mid1=="[ALL]")
{
$mid_min=200;
$mid_max=799;
}

$fd=exec("date +%Y-%m-%d-%H%M%S");

$file='./test/tmp/' . $fd . '.txt';

$f = fopen($file, 'w');
$header = "Freq\t\tMsg\tRX\tShip MMSI\tName\r\n\n";
fwrite($f, $header);

$con=mysqli_connect("localhost","root","","yadd");
// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
 

      $result = mysqli_query($con,"select raw_from_mmsi, from_name, rx_freq, count(*), count(distinct rx_id), from_ctry from newlog where datetime > date_sub(utc_timestamp(), interval ".$timescale." day)  and ( from_mid >= ".$mid_min." and from_mid <= ".$mid_max." ) and from_type = 'SHIP' group by raw_from_mmsi, rx_freq order by ".$order_by.", abs(rx_freq)");
	  
        echo "<br>";
        echo "Text file output for copying into documents/email etc <br>";      
        echo "Click to read or 'Right Click' to Save As...<a href=".$file.">File output</a>  :<br><br>";
	  echo "MID block used : <font color=#541b66>".$mid1."</font><br><br>";
	  
echo "<table border='0' cellpadding='5' rules='rows'>
<tr>
<th> <font face=monospace color=#424242 size='3pt'>MMSI " . $mid1 . "</font></th>
<th><font face=monospace color=#424242 size='3pt'>Ship Station </font></th>
<th><font  face=monospace color=#424242 size='3pt'>Country</font></th>
<th><font  face=monospace color=#424242 size='3pt'>Frequency</font></th>
<th><font  face=monospace color=#424242 size='3pt'>Messages</font></th>
<th><font  face=monospace color=#424242 size='3pt'>Reporters</font></th>
</tr>";

while ($row=mysqli_fetch_array($result)) {

    echo "<tr>";

echo "<td nowrap ><font face=monospace color='blue' size='3pt'><a href='./band_ship_search.php?from_mmsi=" . $row['raw_from_mmsi'] . "&rx_freq=" . $row['rx_freq'] . "'>" . $row['raw_from_mmsi'] . "</a></font></td>";

    echo "<td ><font face=monospace color=#424242 size='3pt'>" . $row['from_name'] . "</font></td>";
    echo "<td ><font face=monospace color=#424242 size='3pt'>" . $row['from_ctry'] . "</font></td>";
    echo "<td ><font face=monospace color=#424242 size='3pt'>" . $row['rx_freq'] . "</font></td>";
    echo "<td ><font face=monospace color=#424242 size='3pt'>" . $row['count(*)'] . "</font></td>";
    echo "<td ><font face=monospace color=#424242 size='3pt'>" . $row['count(distinct rx_id)'] . "</font></td>";
    echo "</tr>";

  
  
  $from_mmsi = $row['raw_from_mmsi'];
  $from_name = $row['from_name'];
  $ctry = $row['from_ctry'];
  $count = $row['count(*)'];
  $rxfreq = $row['rx_freq'];
  $count_rx = $row['count(distinct rx_id)'];
  
  $output = "$rxfreq\t\t$count\t$count_rx\t$from_mmsi\t$from_name, $ctry\r\n";
  
  fwrite($f, $output);
  }
echo "</table>";
echo "</font>";
fclose($f);
mysqli_close($con);
?>





</center>
<center><br><a href="../../index.php">HOME</a>
</body>
</html>
 
