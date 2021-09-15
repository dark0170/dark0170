from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, views1 ,viewsbot, HomeSampleCollectionRMBot_Services, bolt_bot_services
# from nlp_engine import counter_logic


urlpatterns = [

    url('^entity/$', views.Entity_Details, name='entity'),
    url('^entitycreate/$', views.Entity_Create, name='entityCreate'),
    url('^entitydelete/(?P<id>[0-9]+)/$', views.Entity_delete, name='entitydelete'),
    url('^entityedit/(?P<id>[0-9]+)/$', views.Entity_edit, name='entityedit'),
    url('^entityedit1/$', views.Entity_edit1, name='entityedit1'),
    
    url('^dynamic_recom/$', views1.dynamic_recom, name='dynamic_recom'),



    url('^intenttotask/$', views.IntentToTask_Details, name='intenttotask'),
    url('^intenttotaskcreate/$', views.IntentToTask_Create, name='intenttotaskCreate'),
    url('^intenttotaskdelete/(?P<id>[0-9]+)/$', views.IntentToTask_delete, name='intenttotaskdelete'),
    url('^intenttotaskedit/(?P<id>[0-9]+)/$', views.IntentToTask_edit, name='intenttotaskedit'),
    url('^intenttotaskedit1/$', views.IntentToTask_edit1, name='intenttotaskedit1'),

    url('^tasktoentity/$', views.TaskToEntity_Details, name='tasktoentity'),
    url('^tasktoentitycreate/$', views.TaskToEntity_Create, name='tasktoentityCreate'),
    url('^tasktoentitydelete/(?P<id>[0-9]+)/$', views.TaskToEntity_delete, name='tasktoentitydelete'),
    url('^tasktoentityedit/(?P<id>[0-9]+)/$', views.TaskToEntity_edit, name='tasktoentityedit'),
    url('^tasktoentityedit1/$', views.TaskToEntity_edit1, name='tasktoentityedit1'),


  


    url('^nell_bot/$', viewsbot.nell_bot, name='nell_bot'),
    url('^question_view/$',viewsbot.question_view, name='question_view'),
    # url('^feedback/$',viewsbot.update_feedback, name='feedback'),


    
    url('^redisclear/$',viewsbot.redis_clear, name='redis_clear'),
    
    url('^feed_back_thanks/$', views1.feed_back_thanks, name='feed_back_thanks'),
    url('^faq/$', views1.faq_data, name='faq_data'),
    url('^faqCreate/$', views1.faq_Create, name='faq_Create'),
    url('^faqDelete/(?P<id>[0-9]+)$', views1.faq_delete, name='faq_delete'),
    url('^faq_pre/(?P<id>[0-9]+)$', views1.faq_edit_pre, name='faq_edit_pre'),
    url('^faq_edit/$', views1.faq_edit, name='faq_edit'),
    url('^faq_task/$', views1.faq_task, name='faq_task'),





    url('^ConveUserdeleteall/$', views.user_chat_data_ConveUser_delete_all, name='ConveUser_delete_all'),
    url('^UserchatDeleteall/$', views.user_chat_data_delete_all, name='UserChatDataDeleteAll'),

    url('^testtemp/$',views.testtemp, name='testtemp'),
    url('^user_chat_data/$', views.user_chat_data, name='user_chat_data'),
    url('^userchatdatadelete/(?P<id>[0-9]+)/$', views.user_chat_data_delete, name='user_chat_data_delete'),

    url('^ConveUser/$', views.user_chat_ConveUser_data, name='ConveUser'),
    url('^ConveUserdelete/(?P<id>[0-9]+)/$', views.user_chat_data_ConveUser_delete, name='ConveUserdelete'),

    url('^resultmap/$', views.result_map, name='result_map'),
    url('^resultmapcreate/$', views.result_map_create, name='result_map_create'),
    url('^resultmapupdate/(?P<id>[0-9]+)/$', views.result_map_update, name='result_map_update'),
    url('^resultmapdelete/(?P<id>[0-9]+)/$', views.result_map_delete, name='result_map_delete'),
    url('^resultmapupdate1/$',views.result_map_update1, name='result_map_update1'),

    # url('^supportbot/(?P<name>[a-z0-9A-Z]+) (?P<session_key>[a-z0-9A-Z]+)/$', viewsbot.support_bot, name='supportbot'),
###################################### REST API################################################3
    url('^Kapauth/$', viewsbot.Kap_auth_mob, name='Kap_auth'), ########
    url('^mob_bot_launch/$', viewsbot.Kap_auth_mob_bot_launch, name='mob_bot_launch'), # for bot launch or refresh
    url('^mob/$', viewsbot.Kap_auth_mob, name='Kap_auth_mob'), #authcation on login
    url('^Kaptixbot/$', viewsbot.Kaptix_bot, name='Kaptix_bot'), #bot looping ,conversetional flow
    url('^greet/$', viewsbot.greet, name='greet'),

    url('^get_otp/$', views1.otp_sender, name='get_otp'),
    url('^match_otp/$', views1.match_otp, name='match_otp'),

    url('^auto_search/$', views1.auto_search, name='auto_search'),
    url('^collections/$', views1.all_list, name='collections'),
    url('^data/$', views1.has_kb, name='data'),
    url('^no_kb/$', views1.no_kb, name='no_kb'),
    url('^thanks/$', views1.ok_thanks, name='thanks'),
     url('^design/$', views1.flow, name='design'),

    url('^allsurrendervalue/$', views1.all_surrender_value, name='allsurrendervalue'),


    url('^identifier/$', views1.identifier, name='identifier'),
    url('^workflow/$', views1.work_flow_data, name='workflow'),
    
    url('^getworkflow/$', views1.work_flow_data_save, name='getworkflow'),
    url('^get_traindata/$', views1.get_train_data, name='get_traindata'),
    url('^save_traindata/$', views1.save_train_data, name='save_traindata'),



    # url('^submit_responce/$', views1.submit_responce, name='submit_responce'),
    # url('^final_responce/$', views1.final_responce, name='final_responce'),





    url('^get_regex/$', viewsbot.get_entities, name='get_regex'),
    url('^get_task/$', viewsbot.get_task, name='get_task'),
    url('^lead_generation/$', viewsbot.lead_generation, name='lead_generation'),


    url('^get_entity_details/$', viewsbot.get_entity_details, name='get_entity_details'),




  
################################Live User/Agent ###############################
    # url('^liveagent/$', viewsbot.live_agent, name='liveagent'),


    ################################ recommended ###############################
    url('^recommundedview/$', views.recommunded_data_view, name='recommundedview'),
    url('^recommundedcreate/$', views.recommunded_data_create, name='recommundedcreate'),
    url('^recommundededit1/$', views.recommunded_data_edit1, name='recommundededit1'),
    url('^recommundeddelete/(?P<id>[0-9]+)/$', views.recommunded_data_delete, name='recommundeddelete'),
    url('^recommundededit/(?P<id>[0-9]+)/$', views.recommunded_data_edit, name='recommundededit'),
    ###################################### Pension ##############
    url('^request_no/$', views1.request_no, name='request_no'),
    url('^FAQ_training/$', views1.FAQ_training, name='FAQ_training'),
    url('^policyemail/$', views1.policy_email, name='policyemail'),
    url('^surrendervalue/$', views1.surrender_value, name='surrendervalue'),
    ################ Tricontes Services #######
    url('^tricontes_call/$', views1.tricontes_call, name='tricontes_call'),
    url('^tricontes_training/$', views1.tricontes_training, name='tricontes_training'),
    url('^tricontes_ask_question/$', views1.tricontes_ask_question, name='tricontes_ask_question'),
    ################ Tricontes German Services #######
    url('^german_tricontes_call/$', views1.tricontes_german_call, name='german_tricontes_call'),
    url('^german_tricontes_training/$', views1.tricontes_german_training, name='german_tricontes_training'),
    url('^german_tricontes_ask_question/$', views1.tricontes_geraman_ask_question, name='german_tricontes_ask_question'),
    ################ Apricot Services ########
    ###################### Apricot #######################################
    url('^apricot_process/$', views1.apricot_process, name='apricot_process'),
    url('^Archieved_version/$', views1.Archieved_version, name='Archieved_version'),
    url('^customer_care/$', views1.customer_care, name='customer_care'),
    url('^new_updates/$', views1.new_updates, name='new_updates'),
    ###################### NBFC ##################
    ###################NBFC BOT SERVICES################
    url('^salary_loan/$', views1.salary_loan, name='salary_loan'),
    url('^loan_status/$', views1.loan_status, name='loan_status'),
    url('^loan_sanction/$', views1.loan_sanction, name='loan_sanction'),
    #url('^request_demo/$', views1.request_demo, name='request_demo'),

    ###LMS## API
    url('^penal_charges/$', views1.penal_charges, name='penal_charges'),
    url('^current_mode_of_payment/$', views1.current_mode_of_payment, name='current_mode_of_payment'),
    url('^change_mode_of_payment/$', views1.change_mode_of_payment, name='change_mode_of_payment'),
    url('^send_mail_attachment_for_req_no_due_certificate/$', views1.send_mail_attachment_for_req_no_due_certificate, name='send_mail_attachment_for_req_no_due_certificate'),
    url('^outsatnding_amt/$', views1.outsatnding_amt, name='outsatnding_amt'),
    url('^request_waive_charges/$', views1.request_waive_charges, name='request_waive_charges'),
    #url('^new_reduced_emi/$', views1.new_reduced_emi, name='new_reduced_emi'),
   #url('^new_reduced_tenure/$', views1.new_reduced_tenure, name='new_reduced_tenure'),
    url('^emi_tenure/$', views1.emi_tenure, name='emi_tenure'),
    # url('^paying_amt/$', views1.paying_amt, name='paying_amt'),
    url('^principal_amount/$', views1.principal_amount, name='principal_amount'),
    url('^p_payment_mode/$', views1.p_payment_mode, name='p_payment_mode'),
    url('^waive_charges/$', views1.waive_charges, name='waive_charges'),
    url('^db_change_emi_date/$', views1.db_change_emi_date, name='db_change_emi_date'),
    url('^db_next_emi_date/$', views1.db_next_emi_date, name='db_next_emi_date'),
    url('^amount_validator/$', views1.amount_validator, name='amount_validator'),
    ###################OTP########################
    url('^my_otp_match/$', views1.my_otp_match, name='my_otp_match'),
    url('^send_otp_to_mobile/$', views1.send_otp_to_mobile, name='send_otp_to_mobile'),
    url('^send_otp_to_email/$', views1.send_otp_to_email, name='send_otp_to_email'),
    url('^send_mail_attachment_for_statement/$', views1.send_mail_attachment_for_statement, name='send_mail_attachment_for_statement'),
    url('^send_mail_attachment_for_request_invoice/$', views1.send_mail_attachment_for_request_invoice, name='send_mail_attachment_for_request_invoice'),
    url('^send_mail_attachment_for_schedule_amt/$', views1.send_mail_attachment_for_schedule_amt, name='send_mail_attachment_for_schedule_amt'),
    #######################NBFC END#####################
    ################ Nella BOT Services #### start###
    url('^email_sender/$', views1.email_sender, name='email_sender'),
    url('^email_query/$', views1.email_query, name='email_query'),
    url('^request_demo/$', views1.request_demo, name='request_demo'),
    ################ Nella BOT Services #### End###
    ############Whatsapp Service######
    url('^new_whats_app/$', viewsbot.new_whats_app, name='new_whats_app'),
    ####################################
    #################### Sales force bot Service #########
    url('^sales_force_service/$', views1.sales_force_email_service,name='sales_force_service'),
    #####################################################
    url('^choose/$', views1.choose, name='choose'),

    ########
    ###################### synonyms services
    url('^faq_synonyms/$', views1.faq_synonyms, name='faq_synonyms'),
    url('^task_synonym/$', views1.task_synonym, name='task_synonym'),

    ####################### main_db_bot task_action_service ##############################
    url('^task_action_servic/$', views1.task_action_servic, name='task_action_servic'),

    ########
    ###################### Home_Collection_Request_Bot_Services
    url('^hscrmb_getTaskByUser/$', HomeSampleCollectionRMBot_Services.hscrmb_getTaskByUser, name='hscrmb_getTaskByUser'),
    url('^hscrmb_task_action_servic/$', HomeSampleCollectionRMBot_Services.hscrmb_task_action_servic, name='hscrmb_task_action_servic'),
    url('^hscrmb_getYesNoByUser/$', HomeSampleCollectionRMBot_Services.hscrmb_getYesNoByUser, name='hscrmb_getYesNoByUser'),
    url('^hscrmb_getDetailsByUser/$', HomeSampleCollectionRMBot_Services.hscrmb_getDetailsByUser, name='hscrmb_getDetailsByUser'),
    url('^hscrmb_testSlider/$', HomeSampleCollectionRMBot_Services.hscrmb_testSlider, name='hscrmb_testSlider'),
    url('^hscrmb_fetch/$', HomeSampleCollectionRMBot_Services.hscrmb_fetch, name='hscrmb_fetch'),
    url('^hscrmb_fetchOne/$', HomeSampleCollectionRMBot_Services.hscrmb_fetchOne, name='hscrmb_fetchOne'),
    url('^hscrmb_UpdateStatus/$', HomeSampleCollectionRMBot_Services.hscrmb_UpdateStatus, name='hscrmb_UpdateStatus'),
    url('^hscrmb_fetchUpdate/$', HomeSampleCollectionRMBot_Services.hscrmb_fetchUpdate, name='hscrmb_fetchUpdate'),
    url('^hscrmb_AssignStatus/$', HomeSampleCollectionRMBot_Services.hscrmb_AssignStatus, name='hscrmb_AssignStatus'),
    url('^hscrmb_ViewStatus/$', HomeSampleCollectionRMBot_Services.hscrmb_ViewStatus, name='hscrmb_ViewStatus'),
    url('^hscrmb_View_Field_Agent/$', HomeSampleCollectionRMBot_Services.hscrmb_View_Field_Agent, name='hscrmb_View_Field_Agent'),
    url('^hscrmb_Update_View_Field_Agent/$', HomeSampleCollectionRMBot_Services.hscrmb_Update_View_Field_Agent, name='hscrmb_Update_View_Field_Agent'),
    url('^hscrmb_Update_Field_Agent/$', HomeSampleCollectionRMBot_Services.hscrmb_Update_Field_Agent, name='hscrmb_Update_Field_Agent'),
    url('^hscrmb_Update_YesNo_Field_Agent/$', HomeSampleCollectionRMBot_Services.hscrmb_Update_YesNo_Field_Agent, name='hscrmb_Update_YesNo_Field_Agent'),
    url('^hscrmb_Update_Yes_Field_Agent/$', HomeSampleCollectionRMBot_Services.hscrmb_Update_Yes_Field_Agent, name='hscrmb_Update_Yes_Field_Agent'),
    url('^hscrmb_Update_No_Field_Agent/$', HomeSampleCollectionRMBot_Services.hscrmb_Update_No_Field_Agent, name='hscrmb_Update_No_Field_Agent'),




    #############sales_force_bot_services
    url('^bolt_analytics_and_AI/$', bolt_bot_services.bolt_analytics_and_AI,
        name='bolt_analytics_and_AI'),
    url('^bolt_optimization/$', bolt_bot_services.bolt_optimization,
        name='bolt_optimization'),
    url('^bolt_lightning_migration/$', bolt_bot_services.bolt_lightning_migration,
        name='bolt_lightning_migration'),
    url('^bolt_integrations/$', bolt_bot_services.bolt_integrations,
        name='bolt_integrations'),
    url('^bolt_adoption_of_salesforce/$', bolt_bot_services.bolt_adoption_of_salesforce,
        name='bolt_adoption_of_salesforce'),
    url('^bolt_automate_day_to_day_tasks/$', bolt_bot_services.bolt_automate_day_to_day_tasks,
        name='bolt_automate_day_to_day_tasks'),
    url('^bolt_custom_developments/$', bolt_bot_services.bolt_custom_developments,
        name='bolt_custom_developments'),
    url('^bolt_multiple_integrations/$', bolt_bot_services.bolt_multiple_integrations,
        name='bolt_multiple_integrations'),
    url('^bolt_improve_data_strategy/$', bolt_bot_services.bolt_improve_data_strategy,
        name='bolt_improve_data_strategy'),
    url('^bolt_simplify_IT_transformation/$', bolt_bot_services.bolt_simplify_IT_transformation,
        name='bolt_simplify_IT_transformation'),
    url('^bolt_accelerate_application_delivery/$', bolt_bot_services.bolt_accelerate_application_delivery,
        name='bolt_accelerate_application_delivery'),
    url('^bolt_today_products_cloud/$', bolt_bot_services.bolt_today_products_cloud,
        name='bolt_today_products_cloud'),
    url('^bolt_today_products_kanban/$', bolt_bot_services.bolt_today_products_kanban,
        name='bolt_today_products_kanban'),
    url('^bolt_today_products_test_automation/$', bolt_bot_services.bolt_today_products_test_automation,
        name='bolt_today_products_test_automation'),
    url('^bolt_today_products_telecom/$', bolt_bot_services.bolt_today_products_telecom,
        name='bolt_today_products_telecom'),
    url('^bolt_today_products_dashboard/$', bolt_bot_services.bolt_today_products_dashboard,
        name='bolt_today_products_dashboard'),
    url('^bolt_success_stories_case_studies/$', bolt_bot_services.bolt_success_stories_case_studies,
        name='bolt_success_stories_case_studies'),
    url('^bolt_products_cloud/$', bolt_bot_services.bolt_products_cloud,
        name='bolt_products_cloud'),
    url('^bolt_products_kanban/$', bolt_bot_services.bolt_products_kanban,
        name='bolt_products_kanban'),
    url('^bolt_products_test_automation/$', bolt_bot_services.bolt_products_test_automation,
        name='bolt_products_test_automation'),
    url('^bolt_products_telecom/$', bolt_bot_services.bolt_products_telecom,
        name='bolt_products_telecom'),
    url('^bolt_products_dashboard/$', bolt_bot_services.bolt_products_dashboard,
        name='bolt_products_dashboard'),
    url('^bolt_something_else_yes/$', bolt_bot_services.bolt_something_else_yes,
        name='bolt_something_else_yes'),
    url('^bolt_something_else_no/$', bolt_bot_services.bolt_something_else_no,
        name='bolt_something_else_no'),
    url('^bolt_check_out_today_products_service/$', bolt_bot_services.bolt_check_out_today_products_service,
        name='bolt_check_out_today_products_service'),







]
urlpatterns = format_suffix_patterns(urlpatterns)

