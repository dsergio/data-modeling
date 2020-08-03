package com.dsergio.datamodeling.extract;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLData;
import java.sql.SQLException;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class ExtractCAICWeather extends ExtractBase implements IExtract {
	
	private List<LocalDate> dates;
	
	public ExtractCAICWeather(LocalDate startDate, LocalDate endDate, List<Integer> allowedMonths) {
		
		dates = new ArrayList<LocalDate>();
		
		for (LocalDate date : getDatesBetween(startDate, endDate)) {
			if (allowedMonths.contains(date.getMonthValue())) {
//				System.out.println("date: "+ date);
				dates.add(date);
			}
		}
		
		extractObject = new ExtractObjectCAICWeather(dates, allowedMonths);
	}
	
	
	private List<LocalDate> getDatesBetween(LocalDate startDate, LocalDate endDate) {

		long numOfDaysBetween = ChronoUnit.DAYS.between(startDate, endDate);
		return IntStream.iterate(0, i -> i + 1).limit(numOfDaysBetween).mapToObj(i -> startDate.plusDays(i))
				.collect(Collectors.toList());
	}
	
	@Override
	public IExtractObject extractData() {
		
		for (LocalDate date : dates) {
			System.out.println("getCAICWeatherData: " + date);
			getCAICWeatherData(date.toString());
		}
		
		return extractObject;
	}
	
	private void getCAICWeatherData(String date) {
		
		String fileName = "../extract/weather/stage1/weatherdata_" + date + ".csv";
		String baseUrl = "https://avalanche.state.co.us/caic/obs_stns/zones.php?date=" + date + "+11&stnlink=daily&flag=off&area=caic&span=6&unit=m";

		URL urlObj = null;
		try {
			urlObj = new URL(baseUrl);
		} catch (MalformedURLException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
		URLConnection urlCon = null;
		try {
			urlCon = urlObj.openConnection();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

		InputStream inputStream = null;
		try {
			inputStream = urlCon.getInputStream();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		BufferedInputStream reader = new BufferedInputStream(inputStream);

		byte[] contents = new byte[1024];
		int bytesRead = 0;
		String htmlStr = "";
		try {
			while ((bytesRead = reader.read(contents)) != -1) {
				htmlStr += new String(contents, 0, bytesRead);
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		Map<Integer, String> tableOrder = new HashMap<Integer, String>();
		Map<String, Element> pageTables = new HashMap<String, Element>();

		Document doc = Jsoup.parse(htmlStr, "UTF-8");
		
		
		Elements h4Elements = doc.select("h4");
		for (int i = 0; i < h4Elements.size(); i++) {
			Element h4 = h4Elements.get(i);
			System.out.println(h4.text());
			tableOrder.put(i, h4.text());
		}
		
		Elements tables = doc.select("table.sortable");
		for (int i = 0; i < tables.size(); i++) {
			Element t = tables.get(i);
			pageTables.put(tableOrder.get(i), t);
		}
		
		String output = "";
		
		int c = 0, k = 0;
		for (String s : pageTables.keySet()) {
			
			Element t = pageTables.get(s);
			
			Elements rows = t.select("tr");
			
			for (int i = 0; i < rows.size(); i++) {
				
				Element row = rows.get(i);
				Elements cols = null;
				
				String line = "";
				if (i == 0 && k == 0) {
					cols = row.select("th");
					line = "CAIC_Weather_Date,BC Zone,";
				} else {
					cols = row.select("td");
					line = date + "," + s + ",";
				}
				
				
				
				String lineText = "";
				for (int j = 0; j < cols.size(); j++) {
					
					Element td = cols.get(j);
					
					String tdStr = td.text();
					if (tdStr.equals("-")) {
						tdStr = "?";
					}
					
					if (i > 0 && j == 1 && !tdStr.equals("?") && tdStr != null && !tdStr.equals("")) { // elevation
						System.out.println(tdStr);
						int elevation = Integer.parseInt(tdStr);
						if (elevation > 3500) {
							line += ">TL,";
						} else if (elevation < 3000) {
							line += "<TL,";
						} else {
							line += "TL,";
						}
					}
					if (i == 0 && j == 1 && k == 0) {
						line += "ElevTL,";
					}
					
					if (j < cols.size() - 1) {
						line += tdStr + ",";
					} else {
						line += tdStr;
					}
					lineText += tdStr;
				}
				
				if (i < rows.size() - 1) {
					line += "\n";
				}
				if (i == 0 && c == 0 && !lineText.trim().equals("")) {
					output += line;
				}
				if (i > 0 && !lineText.trim().equals("")) {
					output += line;
				} 
				
			}
			
			c++;
			k++;
		}
		System.out.println(output);
		
		PrintWriter writer;
		try {
//			writer = new PrintWriter(fileName, "UTF-8");
			writer = new PrintWriter(new FileOutputStream(new File(fileName), true));

			writer.print(output);
			writer.close();
			
			if (output != null && !output.equals("")) {
				extractObject.addExtractedFileName(fileName);
			}
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
	}
}
