$(function() {

$(".newq").click(function() {
    add();

});

$(".done").click(function() {
    submit();
})




add = function() {
    $(".questions").append($("<div class='question'></div>").html($("script#question").html()));
    $(".mc-options .option > span").click(function() {
        console.log("x");
        $(this).parent().remove();
    })

    $("input.type").on("change", function() {
        nm = $(this).attr("value");
        if(nm == 'mc') {
            $('.mc', $(this).parent()).show();
            $('.fr', $(this).parent()).hide();
        } else if(nm == 'fr') {
            $('.fr', $(this).parent()).show();
            $('.mc', $(this).parent()).hide();
        }
    });

    $(".mc-options .option > span").click(function() {
        $(this).parent().remove();
    })

    $(".mc-options .option").dblclick(function() {
        $(".option", $(this).parent()).removeClass("correct");
        $(this).addClass("correct");
    })


    $(".option-add").click(function() {
        $(this).parent().append("<div class='option' contenteditable=true ondblclick='this.remove()'><span></span>Option</div>");
    })

}

parse = function() {
    data = [];
    var qs = $(".questions > .question");
    qs.each(function() {
        obj = {
            type: $("input.type", $(this)).attr('value'),
            title: $(".title", $(this)).html(),
            tags: $(".tags", $(this)).html().split(' '),
        };
        if(obj.type == 'mc') {
            opts = $(".mc-options > .option", $(this));
            obj['options'] = [];
            opts.each(function() {
                obj['options'].push(o = {
                    html: $(this).html().replace('<span></span>','')
                });
                if($(this).hasClass('correct')) obj['correct'] = o;
            });
        } else if(obj.type == 'fr') {
            opts = $(".mc-options > .option", $(this));
            obj['correct'] = opts.eq(0).html();
            obj['options'] = [obj['correct']];
        }
        data.push(obj);
    });
    return data;
}

send = function(data) {
    var enddate = $("input.enddate").val();
    if(enddate == "") enddate = "9001";
    var testtitle = $(".testtitle").html();
    $.post('/quest/add/submit/', {'data': JSON.stringify(data), 'testtitle': testtitle, 'enddate': enddate}, function() {
        location.href = '/dashboard';
    });
}

submit = function() {
    data = parse();
    console.log(data);
    send(data);
}

$(".newq").click();

});

