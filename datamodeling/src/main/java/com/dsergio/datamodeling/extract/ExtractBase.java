package com.dsergio.datamodeling.extract;

public abstract class ExtractBase implements IExtract {

	protected IExtractObject extractObject;

	public ExtractBase() {
		super();
	}
	
	@Override
	public abstract IExtractObject extractData();

}