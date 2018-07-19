function Search() {
        var namespace = $("input[name=namespace]:eq(0)").val();
        var keys = $("input[name=keys]:eq(0)").val();
        var redistype = $("input[type=radio]:checked").val()
        var data = {"namespace": namespace, "keys": keys, "redistype": redistype};
        if (namespace.length != 0 && keys.length != 0) {
            $.ajax({
                method: "POST",
                url: "/redistools/search/",
                data: data,
                dataType: "html",
                success: function (result) {
                    $("#result").html(result);
                    $("input[name=namespace]:eq(0)").val("");
                    $("input[name=keys]:eq(0)").val("");
                }
            });
        }
        else {
            alert("namespace或keys不能为空")
        }
    }
    function Delete() {
        var namespace = $("input[name=namespace]:eq(0)").val();
        var keys = $("input[name=keys]:eq(0)").val();
        var redistype = $("input[type=radio]:checked").val()
        var data = {"namespace": namespace, "keys": keys, "redistype": redistype};
        console.log(namespace)
        if (namespace.length != 0 && keys.length != 0) {
            if (confirm("确定删除: " + JSON.stringify(data))) {
                $.ajax({
                    method: "POST",
                    url: "/redistools/delete/",
                    data: data,
                    dataType: "html",
                    success: function (result) {
                        $("#result").html(result);
                        $("input[name=namespace]:eq(0)").val("");
                        $("input[name=keys]:eq(0)").val("");
                    }
                });
            }
        }
        else {
            alert("namespace或keys不能为空")
        }
    }