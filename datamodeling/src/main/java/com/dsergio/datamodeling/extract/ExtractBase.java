package com.dsergio.datamodeling.extract;

public abstract class ExtractBase {

	protected IExtractObject extractObject;

	public ExtractBase() {
		super();
	}
	
	public abstract IExtractObject extractData();

}