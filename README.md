# Building a Python client to make REST API calls to the SDS Service

**Version:** 1.2.0

[![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/ADH/aveva.sample-adh-time_series-python?branchName=main)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=2624&branchName=main)

The sample code in this topic demonstrates how to invoke SDS REST APIs using Python. By examining the code, you will see how to create an SdsType and SdsStream, and how to create, read, update, and delete values in SDS. You will also see the effect of the accept verbosity header, summaries value call, and how to do bulk streams calls.

This sample code uses the python `requests` module, which natively supports encoding. As a result, the requests in this sample will automatically include the `Accept-Encoding` header and automatically decompress the encoded responses before returning them to the user, so no special handling is required to support compression.

The sections that follow provide a brief description of the process from beginning to end.

Developed against Python 3.9.1.

## Running the Sample

1. Clone the GitHub repository
1. Install required modules: `pip install -r requirements.txt`
1. Open the folder with your favorite IDE
1. Configure the sample using the file [appsettings.placeholder.json](appsettings.placeholder.json). Before editing, rename this file to `appsettings.json`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.
1. Update `appsettings.json` with the credentials provided by AVEVA
1. Run `program.py`

To Test the sample:

1. Run `python test.py`

or

1. Install pytest `pip install pytest`
1. Run `pytest program.py`

## Configure the Sample

Included in the sample there is a configuration file with placeholders that need to be replaced with the proper values. They include information for authentication, connecting to the SDS Service, and pointing to a namespace.

To run this sample against the Edge Data Store, the sample must be run locally on the machine where Edge Data Store is installed. In addition, the same config information must be entered with the exception of the `ClientId` and `ClientSecret` parameters. For a typical or default installation, the values will be:

- `"Namespace": "default"`
- `"Resource": "http://localhost:5590"`
- `"Tenant": "default"`
- `"ApiVersion": "v1"`

The values to be replaced are in `appsettings.json`:

```json
{
  "Resource": "https://uswe.datahub.connect.aveva.com",
  "ApiVersion": "v1",
  "TenantId": "PLACEHOLDER_REPLACE_WITH_TENANT_ID",
  "NamespaceId": "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID",
  "CommunityId": null,
  "ClientId": "PLACEHOLDER_REPLACE_WITH_APPLICATION_IDENTIFIER",
  "ClientSecret": "PLACEHOLDER_REPLACE_WITH_APPLICATION_SECRET"
}
```

### Community

If you would like to see an example of basic interactions with an ADH community, enter an existing community id in the `Community` field of the configuration. Make sure to also grant the appropriate "Community Member" role to the Client-Credentials Client used by the sample. If you have not yet created a community, see the [documentation](https://docs.osisoft.com/bundle/ocs/page/communities/create-a-community.html) for instructions. Entering a community id will enable three additional steps in the sample.

If you are not using ADH communities, leave the `Community` field blank.

---

Automated test uses Python 3.9.1 x64

For the main ADH time series samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS/blob/main/docs/SDS_TIME_SERIES.md)  
For the main ADH samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OCS)  
For the main AVEVA samples page [ReadMe](https://github.com/osisoft/OSI-Samples)
