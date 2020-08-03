package com.dsergio.datamodeling;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class App {
	
    public static void main( String[] args ) {
    	
    	LocalDate start = LocalDate.of(2017, 12, 1);
		LocalDate end = LocalDate.of(2018, 4, 1);
		List<Integer> allowedMonths = new ArrayList<Integer>();
		allowedMonths.add(1);
		allowedMonths.add(2);
		allowedMonths.add(3);
		allowedMonths.add(12);
		
		ETL etl = new ETL(start, end, allowedMonths);
		
		etl.process();
    }
}
