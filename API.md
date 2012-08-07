REST API Specification
======================

Panel [application/vnd.orchestra.Panel+json]
--------------------------------------------
A Panel represents a user's view of all accessible resources.
A "Panel" resource model contains the following fields:

* **uri**                     _URI_  
    A GET against this URI refreshes the client representation of the resources accessible to this user.

Contact [application/vnd.orchestra.Contact+json]
------------------------------------------------
A Contact represents 

* **uri**                     _URI_
* **name**                    _String_      1
* **surname**                 _String_      0..1
* **second_surname**          _String_      0..1
* **national_id**             _String_      1
* **type**                    _String_      1
* **language**                _String_      1
* **address**                 _String_      1
* **city**                    _String_      1
* **zipcode**                 _Number_      1
* **province**                _String_      1
* **country**                 _String_      1
* **fax**                     _String_      0..1
* **comments**                _String_      0..1
* **emails**                  _String[]_    1
* **phones**                  _String[]_    1
* **billing_contact**         _Contact_     0..1  
    #TODO: phone and emails for this contacts !!
* **technical_contact**       _Contact_     0..1  
    #TODO: this contacts should be equal to Contact on Django models!
* **administrative_contact**  _Contact_     0..1
* **payment**


VirtualHost [application/vnd.orchestra.VirtualHost+json]
--------------------------------------------------------
<TODO: REST and dynamic attributes (resources, contacts)>
A VirtualHost represents an Apache-like virtualhost configuration, which is useful for generating all the configuration files on the web server.
A VirtualHost resource model contains the following fields:

* **server_name**             _String_
* **uri**                     _URI_
* **contact**                 _Contact_
* **ip**                      _String_
* **port**                    _Number_
* **domains**                 _String[]_
* **document_root**           _String_
* **custom_directives**       _String[]_
* **fcgid_user**              _String_
* **fcgid_group string**      _String_
* **fcgid_directives**        _Object_  
    Fcgid custom directives represented on a key/value pairs i.e. {'FcgidildeTimeout': 1202}
* **php_version**             _String_  
* **php_directives**          _Object_  
    PHP custom directives represented on key/value pairs i.e. {'display_errors': 'True'}
* **resource_swap_current**   _Number_  
    PHP custom directives represented on key/value pairs i.e. {'display_errors': 'True'}
* **resource_swap_limit**     _Number_  
    PHP custom directives represented on key/value pairs i.e. {'display_errors': 'True'}
* **resource_cpu_current**    _Number_
* **resource_cpu_limit**      _Number_
* ....


Zone [application/vnd.orchestra.Zone+json]
------------------------------------------
* **origin**                _String_
* **primary_ns**            _String_
* **hostmaster_email**      _String_
* **serial**                _Number_
* **slave_refresh**         _Number_
* **slave_retry**           _Number_
* **slave_expiration**      _Number_
* **min_caching_time**      _Number_
* **records**               _Object[]_  
    Domain record i.e. {'name': ('type', 'value') }


Name [application/vnd.orchestra.Name+json]
------------------------------------------
* **name**                  _String_
* **extension**             _String_
* **register_provider**     _String_
* **name_server**           _Object[]_  
    Name server key/value i.e. {'ns1.pangea.org': '1.1.1.1'}
* **virtual_domain**        _Boolean_   <TODO: is redundant with virtual_domain_type?>
* **virtual_domain_type**   _String_
* **zone**                  _Zone_




