<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
  <head>
    <title>
Live</title>
	<meta http-equiv="refresh" content="120">
  </head>
  <body bgcolor="c8d5e6">
	<basefont face="Ariel">

<center>
<h2> YaDDNet : MF/HF DSC Database</h2>

<h3>This view is of</h3>
<b>All SQL Columns "raw" from the new SQL database. Last 60 minutes<br>
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


	echo "<table cellpadding='5' border='0' rules='all'>
<tr>
	<th> <font face=monospace color=blue size='3pt'>ID</font></th>
	<th> <font face=monospace color=blue size='3pt'>Date  /  UTC</font></th>
	<th> <font  face=monospace color=blue size='3pt'>RX_ID</font></th>
	<th> <font  face=monospace color=blue size='3pt'>RX_FREQ</font></th>
	<th> <font  face=monospace color=blue size='3pt'>FMT</font></th>
	<th> <font  face=monospace color=blue size='3pt'>RAW_TO_MMSI</font></th>
	<th> <font  face=monospace color=blue size='3pt'>TO_TYPE</font></th>
	<th> <font  face=monospace color=blue size='3pt'>TO_MID</font></th>
	<th> <font  face=monospace color=blue size='3pt'>TO_CTRY</font></th>
	<th> <font  face=monospace color=blue size='3pt'>TO_NAME</font></th>
	<th> <font  face=monospace color=blue size='3pt'>CAT</font></th>
	<th> <font  face=monospace color=blue size='3pt'>RAW_FROM_MMSI</font></th>
	<th> <font  face=monospace color=blue size='3pt'>FROM_TYPE</font></th>
	<th> <font  face=monospace color=blue size='3pt'>FROM_MID</font></th>
	<th> <font  face=monospace color=blue size='3pt'>FROM_CTRY</font></th>
	<th> <font  face=monospace color=blue size='3pt'>FROM_NAME</font></th>
	
	<th> <font  face=monospace color=blue size='3pt'>TC1</font></th>

	<th> <font  face=monospace color=blue size='3pt'>TC2</font></th>
	<th> <font  face=monospace color=blue size='3pt'>FREQ</font></th>
	<th> <font  face=monospace color=blue size='3pt'>POS</font></th>
	<th> <font  face=monospace color=blue size='3pt'>EOS</font></th>
	<th> <font  face=monospace color=blue size='3pt'>ECC</font></th>
	<th> <font  face=monospace color=blue size='3pt'>RAW_DSC_MESSAGE</font></th>
	</tr>";

while($row = mysqli_fetch_array($result))
{
    echo "<tr>";
  echo "<td nowrap><font face=monospace size='3pt'>"  . $row['id'] . "</font> </td>";
  echo "<td nowrap><font face=monospace size='3pt'>"  . $row['DATETIME'] . "</font> </td>";

  echo "<td nowrap ><font  face=monospace  size='3pt'>" . $row['RX_ID'] . "</font></td>";
  echo "<td ><font  face=monospace  size='3pt'>" . $row['RX_FREQ'] . "</font></td>";
  echo "<td ><font  face=monospace  size='3pt'>" . $row['FMT'] . "</font></td>";
  echo "<td nowrap ><font  face=monospace size='3pt'>" . $row['RAW_TO_MMSI'] . "</font></td>";
  echo "<td ><font  face=monospace size='3pt'>" . $row['TO_TYPE'] . "</font></td>";
  echo "<td ><font  face=monospace size='3pt'>" . $row['TO_MID'] . "</font></td>";
  echo "<td nowrap><font  face=monospace size='3pt'>" . $row['TO_CTRY'] . "</font></td>";
  echo "<td nowrap><font  face=monospace size='3pt'>" . $row['TO_NAME'] . "</font></td>";
  echo "<td ><font  face=monospace  size='3pt'>" . $row['CAT'] . "</font></td>";
  echo "<td ><font  face=monospace size='3pt'>" . $row['RAW_FROM_MMSI'] . "</font></td>";
  echo "<td ><font  face=monospace size='3pt'>" . $row['FROM_TYPE'] . "</font></td>";
  echo "<td ><font  face=monospace size='3pt'>" . $row['FROM_MID'] . "</font></td>";
  echo "<td nowrap ><font  face=monospace size='3pt'>" . $row['FROM_CTRY'] . "</font></td>";
  echo "<td nowrap><font  face=monospace size='3pt'>" . $row['FROM_NAME'] . "</font></td>";
  echo "<td nowrap ><font  face=monospace  size='3pt'>" . $row['TC1'] . "</font></td>";
  echo "<td nowrap><font  face=monospace  size='3pt'>" . $row['TC2'] . "</font></td>";
  echo "<td nowrap><font  face=monospace  size='3pt'>" . $row['FREQ'] . "</font></td>";
  echo "<td nowrap ><font  face=monospace  size='3pt'>" . $row['POS'] . "</font></td>";
  echo "<td ><font  face=monospace size='3pt'>" . $row['EOS'] . "</font></td>";
  echo "<td ><font  face=monospace size='3pt'>" . $row['ECC'] . "</font></td>";

  
  echo "<td nowrap ><font  face=monospace size='3pt'>" . $row['RAW_DSC_MESSAGE'] . "</font></td>";
  echo "</tr>";  }
echo "</table>";
echo "</font>";

mysqli_close($con);
?>
</center>
<center><br><a href="../../index.php">HOME</a></body>
</html>

