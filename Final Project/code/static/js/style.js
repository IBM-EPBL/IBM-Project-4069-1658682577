<script>
window.watsonAssistantChatOptions = {
integrationID: "1e37e3f8-b996-4518-935d-5d45ea53a543", // The ID of this integration.
region: "au-syd", // The region your integration is hosted in.
serviceInstanceID: "6a00d3de-c85d-45d1-ac93-3662219a5b2b", // The ID of your service instance.
onLoad: function(instance) { instance.render(); }
};
setTimeout(function(){
const t=document.createElement('script');
t.src="https://web-chat.global.assistant.watson.appdomain.cloud/versions/" + (window.watsonAssistantChatOptions.clientVersion || 'latest') + "/WatsonAssistantChatEntry.js";
document.head.appendChild(t);
});
</script>
