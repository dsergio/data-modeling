package com.dsergio.datamodeling.extract;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class ExtractObjectCAICWeather implements IExtractObject {
	
	private List<LocalDate> dates;
	private List<Integer> allowedMonths;
	private List<String> extractedFileNames;
	
	public ExtractObjectCAICWeather(List<LocalDate> dates, List<Integer> allowedMonths) {
		this.dates = dates;
		this.allowedMonths = allowedMonths;
		extractedFileNames = new ArrayList<String>();
	}
	
	@Override
	public void addExtractedFileName(String fileName) {
		extractedFileNames.add(fileName);
	}

	public List<LocalDate> getDates() {
		return dates;
	}

	public List<Integer> getAllowedMonths() {
		return allowedMonths;
	}
	
	@Override
	public List<String> getExtractedFileNames() {
		return extractedFileNames;
	}

}
