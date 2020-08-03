package com.dsergio.datamodeling.extract;

import java.util.List;

public interface IExtractObject {

	void addExtractedFileName(String fileName);

	List<String> getExtractedFileNames();

}