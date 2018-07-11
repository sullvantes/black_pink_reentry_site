String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};


jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

    //evaluate each client day for a walkstring
    $("input[name^='form-'][name $='_walks']").each(function(){
        evalWalkString(this);
        var id = this.id.replace(/id_form-/, '').replace(/_walks/,'');
    });

    $("input[name^='form-'][name $='-all_pay']").each(function(){
        var id = this.name.replace(/form-/, '').replace(/-all_pay/,'');
        evalClientWeek(id);
    });
    
    // evalTotals();
    // evalHours();

    function evalWalkString(object){
        var str = object.value.toUpperCase();
        var id = object.id.replace(/id_form-/, '').replace(/_walks/,'');
        var description = "";
        var rate = parseFloat(document.getElementById('id_rate').value);
        var extra = parseFloat(2.00)
        var walk_count = 0;
        var day_owed = 0.00;
        var dogs = parseFloat(document.getElementById('id_form-' +id.split('-')[0] + '-default_dogs').value)
        
        legend = [['X', "Single Dog", rate], 
                    ['Y', "Two Dog",rate + extra],
                    ['Z', "Three Dog", rate + 2 * extra],
                    ['A', "Four Dog",rate + 3 * extra],
                    ['O', "Not Cancelled", rate + (dogs-1)* extra],
                    ['H', "Half", parseFloat(5.5)],
                    ['NC', "No Charge To Client", rate + (dogs-1)* extra]
                ]
        for (var i = 0; i< legend.length; i++){
            walk_char = legend[i][0];
            walk_type = legend[i][1];
            walk_rate = legend[i][2];
            
            if (str.includes(walk_char)){
                var re = new RegExp(walk_char, 'g');
                these_walks = (str.match(re) || []).length;
                if (these_walks == 1 ){
                    description += "<span style = 'display: inline-block'>-"+these_walks + " " + walk_type+ " Walk</span><br>"
                } 
                else {
                    description += "<span style = 'display: inline-block'>-"+these_walks + " " + walk_type + " Walks</span><br>"
                }
                str = str.replaceAll(walk_char, '')
                day_owed +=these_walks*walk_rate
                walk_count += these_walks   
            }    
        }         

        if( str ){
            description = "There are invalid characters: " + str.split("") +"."
            day_owed = "0"
            // document.getElementById('id_form-'+id+'-all_pay').value= parseFloat(0.00)
            // id_form-0-all_pay
        }
        
        document.getElementById('id_form-' +id + '_pay').value=day_owed
        if (day_owed){
            document.getElementById('walk_calc_pop_client'+id).innerHTML="$"+ day_owed + ": "+description;
        }
        else{
            document.getElementById('walk_calc_pop_client'+id).innerHTML='';
        }
            document.getElementById('walk_count_client'+id).innerHTML=walk_count;
    };

    // Reevaluate client_week_totals
    function evalClientWeek(id){
        days = ['mon','tues','wed','thu','fri','oth']
        client_week_pay = 0.00
        client_week_walks = 0.00
        for (var i =0; i < days.length;i++){
            client_week_pay += parseFloat(document.getElementById('id_form-'+id+'-'+days[i]+'_pay').value);
            client_week_walks += parseFloat(document.getElementById("walk_count_client"+id+"-"+days[i]).innerHTML);
        } 
        // document.getElementById('id_form-'+id+'-mon_pay').value);
        document.getElementById('id_form-'+id+'-all_pay').value= client_week_pay
        document.getElementById("walk_count_client"+id+"-all").innerHTML= client_week_walks
    }

    function evalHours(id){
        var totalHours = 0.00
        $("input[id ^= 'id_form-'][id $='-hours']").each(function(){
            if (!isNaN($(this).val())){
                totalHours+=parseFloat($(this).val());
            }
        });
        document.getElementById('id_total_hours').value= parseFloat(totalHours);
    }

    function evalTotals(){
        // totalPay
        var totalPay = 0.00;
        $("input[id ^= 'id_form-'][id $='-all_pay']").each(function(){
            totalPay+=parseFloat($(this).val());
        });
        transp_reimb_rate = parseFloat(document.getElementById('id_transportation_reimbursement').value)
        // other_adjustment = parseFloat(document.getElementById('id_other_adjustment').value)
        document.getElementById('id_total_owed').value=totalPay+transp_reimb_rate
        var totalWalks = 0;
        $("div[id ^='walk_count_client'][id $='-all']").each(function(){
            totalWalks+=parseFloat($(this).html());
        });
        document.getElementById('id_total_walks').value=parseFloat(totalWalks)
    }

    
    // when a client hours changes
    $("input[id ^= 'id_form-'][id $='-hours']").change(function(){
        evalHours();
    });

    // When a client week changes
    $("div[id ^='walk_count_client'][id $='-all']").change(function(){
        evalTotals()
    });
    // When a client day pay changes
    $("input[name^='form-'][name $='_pay']").change(function(){
        var id = this.id.replace(/id_form-/, '').replace(/_walks/,'');
        evalClientWeek(id.split('-')[0]);
        evalTotals()
    });

    // When a client day string changes
    $("input[name^='form-'][name $='_walks']").change(function(){
        evalWalkString(this);
        var id = this.id.replace(/id_form-/, '').replace(/_walks/,'');
        evalClientWeek(id.split('-')[0]);
        evalTotals();    
    });


    $('#iprog_button').click(function(){
        document.getElementById('id_status').value = 'IPROG'
        document.getElementById('go_home').value = '1'
        console.log("in Progress")
        $( '#walk_rpt_form').submit();
    });

    $('#unsbmt_button').click(function(){
        document.getElementById('id_status').value = 'IPROG'
        document.getElementById('go_home').value = '0'
        console.log("in Progress")
        $( '#walk_rpt_form').submit();
    });


    $('#sbmt_button').click(function(){
        document.getElementById('id_status').value = 'SBMT'
        document.getElementById('go_home').value = '1'
        console.log("submitted")
        $( '#walk_rpt_form').submit();
    });
   
    
    $('#unappr_button').click(function(){
        document.getElementById('id_status').value = 'APPR'
        document.getElementById('go_home').value = '0'
        console.log("approved")
        $( '#walk_rpt_form').submit();

    });
    
    $('#appr_button').click(function(){
        document.getElementById('id_status').value = 'APPR'
        document.getElementById('go_home').value = '1'
        console.log("approved")
        $( '#walk_rpt_form').submit();

    });

});

