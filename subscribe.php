<?php
// FitCafe Subscription Proxy
// Forwards subscription to Listmonk and redirects back to main site

// Get the raw POST data
$postData = file_get_contents('php://input');

// If no raw data, use $_POST
if (empty($postData)) {
    $postData = http_build_query($_POST);
}

// Forward to Listmonk
$ch = curl_init('https://listmonk.thequietself.com/subscription/form');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/x-www-form-urlencoded'
));
curl_exec($ch);
// Note: curl_close() is deprecated in PHP 8.5+, so we skip it
// curl_close($ch);

// Redirect to main site with success parameter
header('Location: https://fitcafecoffee.com?subscribed=true');
exit;
?>