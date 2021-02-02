$(document).ready(function () {
    $('.sidenav').sidenav({ edge: "right" });
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $('input#input_text, textarea#textarea2').characterCounter();
    $('select').formSelect();

    // This function allows the user to click for more rows as they input their steps to preparing the recipe
    $("#add_button").click(function () {
        $(".method_steps").append(
            `<li><textarea id="method" name="method" type="text" class="validate materialize-textarea" required></textarea><label for="method">Delete Step <a href='javascript:void(0);' class='remove'>&times;</a></label></li>`
        );
        $("#first_method").empty();
        $("#first_method").text("Delete Step ") 
        $("#first_method").append(`<a href='javascript:void(0);' class='remove'>&times;</a>`)
    });
    $(document).on("click", "a.remove", function () {
        $(this).parent().parent().remove();
    });
});