<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Search</title>
    <meta http-equiv="Content-Type" content="text/html" />
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script language="javascript">

function selectallCHBoxr(){ 

if($('#selectallr').attr('checked')){
var inputs = document.getElementsByClassName('rxid');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =true; 
 } }
}
else {
var inputs = document.getElementsByClassName('rxid');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =false; 
} }

}

}

function manualr() {
var inputs = document.getElementsByName('selectallr');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =false; 
} }

}


function selectallCHBoxf(){ 

if($('#selectallf').attr('checked')){
var inputs = document.getElementsByClassName('freq');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =true; 
 } }
}
else {
var inputs = document.getElementsByClassName('freq');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =false; 
} }

}

}

function manualf() {
var inputs = document.getElementsByName('selectallf');
var checkboxes = [];
for (var i = 0; i < inputs.length; i++) {

  if (inputs[i].type == 'checkbox') {
inputs[i].checked =false; 
} }

}




</script>
<style>

 #freq{
color: #424242;
background: #006666;
width:60px;
height:30px;
border-radius: 10px
}
 #rx {
color: #424242;
background: #6666cc;
width:140px;
height:30px;
border-radius: 10px
}
#link {
color: #424242;
background: #6699cc;
width:140px;
height:30px;
border-radius: 10px;
font-weight: bold;
}
#dis {
color: #b0b0b0;
background: #d0d0d0;
width:140px;
height:30px;
border-radius: 10px
}
input[type=submit]{
color: #424242;
background: #003366;
width:60px;
height:30px;
border-radius: 10px
font-weight: bold;
}
select {
color: #424242;
background: #6699cc;
border-radius: 10px;
height: 30px;

font-weight: bold;
}
input[type=text]{
color: #424242;
background: #cccccc;
width:140px;
height:30px;
border-radius: 10px;
border-width: 1px;
font-family: monospace;
font-size: 15px;
font-weight: bold;
padding-left: 10px;
}

 

</style>
</head>
<body bgcolor="c8d5e6">
	<basefont face="Arial">
<center>
<h3>DSC Message search</h3>
<b>Default selections shown in <font color=#424242>WHITE</font></b>
<hr width=50%>
    <form action="./search_rx_table.php" method="GET">
<table cellpadding="5">


<tr>
<td>
Year<br>
<select name="year">
<option value="%" selected >All</option>
<option value="2017" >2017</option>
<option value="2018" >2018</option>
</select>
</td>
<td>
Month<br>
<select name="month">
<option value="%" selected>All</option>
<option value="01">Jan</option>
<option value="02">Feb</option>
<option value="03">Mar</option>
<option value="04">Apr</option>
<option value="05">May</option>
<option value="06">Jun</option>
<option value="07">Jul</option>
<option value="08">Aug</option>
<option value="09">Sep</option>
<option value="10">Oct</option>
<option value="11">Nov</option>
<option value="12">Dec</option>
</select>
</td>

<td>
Day<br>
<select name="day">
<option value="%" selected>All</option>
<option value="01">1</option>
<option value="02">2</option>
<option value="03">3</option>
<option value="04">4</option>
<option value="05">5</option>
<option value="06">6</option>
<option value="07">7</option>
<option value="08">8</option>
<option value="09">9</option>
<option value="10">10</option>
<option value="11">11</option>
<option value="12">12</option>
<option value="13">13</option>
<option value="14">14</option>
<option value="15">15</option>
<option value="16">16</option>
<option value="17">17</option>
<option value="18">18</option>
<option value="19">19</option>
<option value="20">20</option>
<option value="21">21</option>
<option value="22">22</option>
<option value="23">23</option>
<option value="24">24</option>
<option value="25">25</option>
<option value="26">26</option>
<option value="27">27</option>
<option value="28">28</option>
<option value="29">29</option>
<option value="30">30</option>
<option value="31">31</option>

</select>
</td>

</tr>

</table>
<hr width=50%>


<tr>

Select freq: <br>
<input type="checkbox" class="freq" name="selectallf"  id="selectallf" onClick="selectallCHBoxf();" value="TEST" checked /><label for="selectallf"></label>  <font color=#424242>Select All</font><br>
<table>
<tr>
<td><input type="checkbox" id="f1" name="f1" class="freq" value="2177.0" onclick="manualf();" checked /><label for="f1"></label>  2177.0 </td>
<td><input type="checkbox" id="f2" name="f2" class="freq" value="2182.0" onclick="manualf();" checked /><label for="f2"></label>  2182.0 </td>
</tr>
<tr>
<td><input type="checkbox" id="f3" name="f3" class="freq"  value="2187.5" onclick="manualf();" checked /><label for="f3"></label>  2187.5 </td>
<td><input type="checkbox" id="f4" name="f4" class="freq"  value="4207.5" onclick="manualf();" checked /><label for="f4"></label>  4207.5 </td>
<td><input type="checkbox" id="f5" name="f5" class="freq"  value="6312.0" onclick="manualf();"  checked /><label for="f5"></label>  6312.0 </td>
<td><input type="checkbox" id="f6" name="f6" class="freq"  value="8414.5" onclick="manualf();" checked /><label for="f6"></label>  8414.5 </td>
<td><input type="checkbox" id="f7" name="f7" class="freq"  value="12577.0"  onclick="manualf();" checked /><label for="f7"></label>  12577.0 </td>
<td><input type="checkbox" id="f8" name="f8" class="freq"  value="16804.5"  onclick="manualf();" checked /><label for="f8"></label>  16804.5 </td>
</tr>

</table>
<hr width=30%>

<table>
<th>Enter (partial) RX ID</th>

<tr>
<td><center>Use % as wildcard<br>
<input type="text" name="rxid">
</center>
</td>
</tr>
</table>

<hr width=50%>

<table rules="cols">

<th>Results<br>Range</th>
<th>Results<br>Order</th>
<tr>

<td>

<select name="limit">
<option value="0,1000000">All</option>
<option value="0, 20" selected>0-20</option>
<option value="0, 100">0-100</option>
<option value="100, 100">100-200</option>
<option value="200, 100">200-300</option>

</td>
<td>
<input type="radio" name="order" value="desc" checked><font color=#424242>Newest first</font><br>
<input type="radio" name="order" value="asc">Oldest first

</td></tr>

</table>
<hr width=50%>
<input id="link" type="submit" value="Search" />
<br>
<hr width=50%>
<input id="link" type="reset" value="Reset" />
</form>


</center>
<center><br><a href="../../index.php">HOME</a></body>
</html>
