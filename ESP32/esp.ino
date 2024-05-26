#if ! (ESP8266 || ESP32 )
  #error This code is intended to run on the ESP8266/ESP32 platform! Please check your Tools->Board setting
#endif

char ssid[] = "Galaxy4";             // your network SSID (name)
char pass[] = "12345678";         // your network password

char user[]         = "mincoding";          // MySQL user login username
char password[]     = "1234";          // MySQL user login password

#define MYSQL_DEBUG_PORT      Serial

// Debug Level from 0 to 4
#define _MYSQL_LOGLEVEL_      1

#include <MySQL_Generic.h>
#include <SPI.h>
#define USING_HOST_NAME     false

#if USING_HOST_NAME
  // Optional using hostname, and Ethernet built-in DNS lookup
  char SQL_server[] = ""; // change to your server's hostname/URL
#else
  IPAddress SQL_server(3,39,234,126);
#endif

uint16_t server_port = 3306;    //3306;


char default_database[] = "esp32";           //"test_arduino";
char default_table[]    = "item";          //"test_arduino";

MySQL_Connection conn((Client *)&client);
MySQL_Query *query_mem;
MySQL_Query sql_query = MySQL_Query(&conn);

int trigPin = 25;
int echoPin = 26;



void setup()
{
  Serial.begin(115200);

  // MYSQL_DISPLAY1("\nStarting Basic_Insert_ESP on", ARDUINO_BOARD);
  // MYSQL_DISPLAY(MYSQL_MARIADB_GENERIC_VERSION);

  // // Begin WiFi section
  // MYSQL_DISPLAY1("Connecting to", ssid);
  
  WiFi.begin(ssid, pass);
  
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    // MYSQL_DISPLAY0(".");
  }

  // print out info about the connection:
  // MYSQL_DISPLAY1("Connected to network. My IP address is:", WiFi.localIP());

  // MYSQL_DISPLAY3("Connecting to SQL Server @", SQL_server, ", Port =", server_port);
  // MYSQL_DISPLAY5("User =", user, ", PW =", password, ", DB =", default_database);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  SPI.begin(SCK, MISO, MOSI, SS);
  SPI.setFrequency(16000000);
  digitalWrite(SS, LOW);

}


String query = "";
String INSERT_SQL = "";
long duration, distance;
void loop() {
 
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 17 / 1000;
  Serial.print(distance);
  Serial.println("CM");

  query = "SELECT * FROM minDB.command ORDER BY id DESC LIMIT 1";

  if (conn.connectNonBlocking(SQL_server, server_port, user, password) != RESULT_FAIL) {
    runQuery();
  } else {
    MYSQL_DISPLAY("\nConnect failed. Trying again on next iteration.");
  }

  INSERT_SQL = "UPDATE minDB.sensor SET num1 = distance WHERE id = 1";
  
  int distanceIndex = INSERT_SQL.indexOf("distance");
  if (distanceIndex != -1) { // "'distance'" 문자열을 찾았을 때만 대체
    INSERT_SQL = INSERT_SQL.substring(0, distanceIndex) + distance +" " + INSERT_SQL.substring(distanceIndex + 9);
  }

  if (conn.connectNonBlocking(SQL_server, server_port, user, password) != RESULT_FAIL)
  {
    // delay(500);
    runInsert();
  } 
  else 
  {
    MYSQL_DISPLAY("\nConnect failed. Trying again on next iteration.");
  }

  delay(50);

}

uint8_t readData;
char command;
void runQuery()
{
  MYSQL_DISPLAY("====================================================");
  MYSQL_DISPLAY("> Running SELECT with dynamically supplied parameter");
  
  // Supply the parameter for the query
  // Here we use the QUERY_POP as the format string and query as the
  // destination. This uses twice the memory so another option would be
  // to allocate one buffer for all formatted queries or allocate the
  // memory as needed (just make sure you allocate enough memory and
  // free it when you're done!).
  
  MYSQL_DISPLAY(query);
  
  // Initiate the query class instance
  MySQL_Query query_mem = MySQL_Query(&conn);
  
  // Execute the query
  // KH, check if valid before fetching
  // 쿼리 실행
  if ( !query_mem.execute(query.c_str()) )
  {
    MYSQL_DISPLAY("Querying error");
    return;
  }
  
  // Fetch the columns and print them
  column_names *cols = query_mem.get_columns();
  // 쿼리 조건에 해당하는 데이터 열 가져옴
  
  for (int f = 0; f < cols->num_fields; f++) 
  {
    Serial.print("f :");
    Serial.println(f);
    
    MYSQL_DISPLAY0(cols->fields[f]->name);
    
    if (f < cols->num_fields - 1) 
    {
      MYSQL_DISPLAY0(",");
    }
  }


  MYSQL_DISPLAY();
  String text = "";
  String thirdValue ="";
  // Read the rows and print them
  row_values *row = NULL;

  //row 가 NULL 이 될때까지 반복
  do 
  {
    row = query_mem.get_next_row();
    
    if (row != NULL) 
    {
      for (int f = 0; f < cols->num_fields; f++) 
      {
        MYSQL_DISPLAY0(row->values[f]);
        text += row->values[f];
        if (f < cols->num_fields - 1) 
        {
          MYSQL_DISPLAY0(",");
          text += ",";
        }
      }
      Serial.println();
      Serial.print("SQL read : ");
      Serial.println(text);
      int firstCommaIndex = text.indexOf(',');
      int secondCommaIndex = text.indexOf(',', firstCommaIndex + 1);
      int thirdCommaIndex = text.indexOf(',', secondCommaIndex + 1);
  
      // 세 번째 값을 가져오기
      thirdValue = text.substring(secondCommaIndex + 1, thirdCommaIndex);
  
      // 결과 출력
      Serial.println("세 번째 값: " + thirdValue);
      MYSQL_DISPLAY();
    }
  } while (row != NULL);

  if(distance < 15){
    readData = SPI.transfer('f');
  }else{
    if( thirdValue.equals("GO") ){
        readData = SPI.transfer('w');
    }
    if( thirdValue.equals("BACK") ){
       readData = SPI.transfer('x');
    }
  }

  if( thirdValue.equals("LEFT")){
      readData = SPI.transfer('a');
  }
  if( thirdValue.equals ("MID") ){
      readData = SPI.transfer('s');
  }
  if( thirdValue.equals("RIGHT") ){
      readData = SPI.transfer('d');
  }
  if( thirdValue == "STOP" ){
      readData = SPI.transfer('f');
  }
  

}







void runInsert()
{
  // Initiate the query class instance
  MySQL_Query query_mem = MySQL_Query(&conn);

  if (conn.connected())
  {
    MYSQL_DISPLAY(INSERT_SQL);
    
    // Execute the query
    // KH, check if valid before fetching
    if ( !query_mem.execute(INSERT_SQL.c_str()) )
    {
      MYSQL_DISPLAY("Insert error");
    }
    else
    {
      MYSQL_DISPLAY("Data Inserted.");
    }
  }
  else
  {
    MYSQL_DISPLAY("Disconnected from Server. Can't insert.");
  }
}