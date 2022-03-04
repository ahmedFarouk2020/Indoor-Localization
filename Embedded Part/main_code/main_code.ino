#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

WiFiClient client;
HTTPClient http;

int AvailableNetworks;
int timeout = 0;

String ssid;
String password;

String RootDir = "http://192.168.246.5:5000/";
String serverPath = "http://192.168.246.5:5000/api/send-data?";
String Readings = "ap1=" ;

String routers_ssid[6] = {"STUDBME1","STUDBME2","CMP_LAB1","CMP_LAB2","CMP_LAB3","CMP_LAB4"};

// password of STUDBME2 BME2Stud

String Get_String() 
{
    while(!Serial.available());
    String str = Serial.readString();
    str.trim();
    return str;
}

void connect_wifi() 
{
    Serial.print("Please enter the username: ");
    ssid = Get_String();
    Serial.println(ssid);
    Serial.print("Please enter the password: ");
    password = Get_String();
    Serial.println(password);
    Serial.print("Connecting");
    
    WiFi.begin(ssid, password);
//    WiFi.begin("youssef1", "12345678");
    timeout = 0;
    while(WiFi.status() != WL_CONNECTED && timeout < 20) 
    {
      Serial.print(".");
      delay(500);
      timeout++;
    }
    Serial.println("");
    
    if(timeout >= 20)
    {
      Serial.println("Connection failed, please Re-enter ssid & password.");
      connect_wifi();
    }
    
    Serial.print("Connected to WiFi network with IP Address: ");
    Serial.println(WiFi.localIP());
}

void setup() 
{
  Serial.begin(115200);
  
  AvailableNetworks = WiFi.scanNetworks();
  Serial.print("Found ");
  Serial.print(AvailableNetworks);
  Serial.println("Networks: ");
  
  for (int i=0; i<AvailableNetworks; i++)
  {
    Serial.println("SSID : ");
    Serial.println(WiFi.SSID(i));
    Serial.print("Signal Strenth : ");
    Serial.println(WiFi.RSSI(i));
    Serial.println("------------------------");
  }
  
//  connect_wifi();

  http.begin(client, RootDir);
}


void loop() 
{
  int routers_strength[6] = {0,0,0,0,0,0};
   //Check WiFi connection status
  if(WiFi.status()== WL_CONNECTED)
  {
    
    AvailableNetworks = WiFi.scanNetworks();
    for (int i=0; i<AvailableNetworks; i++)
    {
      
      Serial.print("ssid: ");
      Serial.println(WiFi.SSID(i));
      
      Serial.print("RSSI: ");
      Serial.println(WiFi.RSSI(i));
      
      for (int j=0;j<6;j++)
      {  
        if(routers_ssid[j] == WiFi.SSID(i))
        {
          
          routers_strength[j] = WiFi.RSSI(i);
          Serial.printf(" routers_strength: %s",routers_strength[j]);
//          Serial.printf("SSID %d Found %s With Strength: %d\n",j,routers_ssid[j],routers_strength[j]);
          Serial.println("------------------------------");
        }
      }
    }
//    routers_strength[0] = -50;
    Readings += String(routers_strength[0]);
    for(int j = 1; j<6;j++)
    {
        Readings += "&ap" + String(j+1) + "=" + String(routers_strength[j]);
    }
    Serial.println(Readings);
    serverPath += Readings;
    Serial.println(serverPath);
    Readings = "ap1=" ;
    serverPath = "http://192.168.246.5:5000/api/send-data?";
    Serial.println("=======================================================");
    http.begin(client, "http://192.168.246.5:5000/api/send-data?ap1="+ String(routers_strength[0]) +"&ap2="+String(routers_strength[1])+
                        "&ap3="+String(routers_strength[2])
                        +"&ap4="+String(routers_strength[3])+"&ap5="+String(routers_strength[4])+"&ap6="+String(routers_strength[5]));
    int httpResponseCode = http.GET(); 
    Serial.println(httpResponseCode);
    String payload = http.getString();
//      Serial.println(payload);
      // Your Domain name with URL path or IP address with path
      delay(2000);
      // Free resources
      http.end();
      
    }
    else
    {
      Serial.println("WiFi Disconnected");
      connect_wifi();
//    WiFi.begin("youssef1", "12345678");
      delay(5000);
    }
  
}
