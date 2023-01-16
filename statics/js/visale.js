items = document.getElementsByClassName("master");
for(i = 0;i < items.length;i++)
{
    if(document.getElementById("user2").innerText == "admin")
    {
        items[i].style["display"] = "inline";
    }
    else
    {
        items[i].style["display"] = "none";
    }
}
items2 = document.getElementsByClassName("customer-li")
for(i = 0;i < items2.length;i++)
{
    if(document.getElementById("user2").innerText.substring(0,8) == "customer")
    {
        items2[i].style["display"] = "inline";
    }
    else
    {
        items2[i].style["display"] = "none";
    }
}
items3 = document.getElementsByClassName("master");
for(i = 0;i < items3.length;i++)
{
    
    if(document.getElementById("user").innerText == "admin" || document.getElementById("user").value == "admin")
    {
        items3[i].style["display"] = "inline";
    }
    else
    {
        items3[i].style["display"] = "none";
    }
}
items5 = document.getElementsByClassName("customer-li")
for(i = 0;i < items5.length;i++)
{
    if(document.getElementById("user").innerText.substring(0,8) == "customer"|| document.getElementById("user").value.substring(0,8) == "customer")
    {
        items5[i].style["display"] = "inline";
    }
    else
    {
        items5[i].style["display"] = "none";
    }
}
items4 = document.getElementsByClassName("market")
for(i = 0;i < items4.length;i++)
{
    if(document.getElementById("user").innerText == "market"|| document.getElementById("user").value == "market")
    {
        items4[i].style["display"] = "inline";
    }
}
items6 = document.getElementsByClassName("market")
for(i = 0;i < items6.length;i++)
{
    if(document.getElementById("user2").innerText == "market")
    {
        items6[i].style["display"] = "inline";
    }
}
items7 = document.getElementsByClassName("master-market")
for(i = 0;i < items7.length;i++)
{
    if(!(document.getElementById("user").innerText.substring(0,8) == "customer"|| document.getElementById("user").value.substring(0,8) == "customer"))
    {
        items7[i].style["display"] = "inline";
    }
    else
    {
        items7[i].style["display"] = "none";
    }
}
items6 = document.getElementsByClassName("master-market")
for(i = 0;i < items6.length;i++)
{
    if(document.getElementById("user2").innerText.substring(0,8) != "customer")
    {
        items6[i].style["display"] = "inline";
    }
    else
    {
        items6[i].style["display"] = "none";
    }
}
var cond = -1;
var text = "";
function addcond(){
    cond += 1;
    text = "key"+(cond+1)+":<input type='text' name='conds"+cond+"'>value"+(cond+1)+":<input type='text' name='val"+cond+"'><br>";
    if(cond>=9)
    {
        alert("out of range!");
    }
    else
    {
        document.getElementById("cond"+cond).innerHTML = text;
    }
}