Dropzone.autoDiscover = false;
var myDropzone = new Dropzone("#ipa_file", { 
	url: "/check/ipa_upload/",
	maxFilesize: 1024,
	acceptedFiles: '.ipa',
	maxFiles: 5,
	success: function(d, data) {
		data = JSON.parse(data);
		if (data.success == 1) {
			//显示app信息
			$('#app_name').text(data.data.name);
			$('#version').text(data.data.version);
			$('#bundle_identifier').text(data.data.bundle_id);
			$('#target_os_version').text(data.data.tar_version);
			$('#minimum_os_version').text(data.data.min_version);
			//显示ipa的架构信息
			$('#app_arcs').text(data.data.arcs.join(' / '));
			$('#minimum_os_version').text(data.data.min_version);
			$('#profile_type').text(data.data.profile_type);
			$('#expiration').text(data.data.expiration);
			//显示私有api信息
			// doc_apis.append({"api_name": api['ZTOKENNAME'], "class_name": container_name, "type": api['ZTOKENTYPE'],
            //              "header_file": header_path, "source_sdk": version, "source_framework": framework_name, })
			$('#api_in_app div.api_section').remove();
			for (var i = 0; i < data.data.methods_in_app.length; i++) {
				var api = data.data.methods_in_app[i];
				var html = '<div class="api_section section__text mdl-cell mdl-cell--10-col-desktop mdl-cell--6-col-tablet mdl-cell--3-col-phone">' + 
                  '<h5>' + (i + 1) + '、' + api.api_name + '</h5>' + 
                  'api is ' + api.type + ', IN sdk ' + api.source_sdk + '、' + api.source_framework + ' -> ' + api.header_file + ' -> ' + api.class_name + ' -> '+ api.api_name +
                '</div>';
                $('#api_append_div').append(html);
			};
			$('#framework_in_app div.api_section').remove();
			for (var i = 0; i < data.data.private_framework.length; i++) {
				var framework = data.data.private_framework[i];
				var html = '<div class="api_section section__text mdl-cell mdl-cell--10-col-desktop mdl-cell--6-col-tablet mdl-cell--3-col-phone">' + 
                  '<h5>' + (i + 1) + '、' + framework + '</h5>' + 
                '</div>';
                $('#framework_append_div').append(html);
			};
		}
		else {
			alert(data.data);
		}
	}
});