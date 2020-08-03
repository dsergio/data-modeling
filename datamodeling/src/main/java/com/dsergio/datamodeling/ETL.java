package com.dsergio.datamodeling;

import java.time.LocalDate;
import java.util.List;

import com.dsergio.datamodeling.extract.ExtractCAICWeather;
import com.dsergio.datamodeling.extract.IExtract;
import com.dsergio.datamodeling.extract.IExtractObject;

public class ETL {
	
	private IExtract extract;
	private IExtractObject extractObject;
	
	
	public ETL(LocalDate start, LocalDate end, List<Integer> allowedMonths) {
		extract = new ExtractCAICWeather(start, end, allowedMonths);
	}

	public void process() {
		extractObject = extract.extractData();
	}

}
