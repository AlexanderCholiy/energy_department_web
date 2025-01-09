$(document).ready(function() {
    // Инициализация DataTable
    var table = $('#DataTable').DataTable({
        dom: '<"top"lf<"buttons"B>>' + // Элементы управления (количество записей, поиск) и кнопки
            '<"table-responsive"t>' + // Таблица
            '<"bottom"ip>', // Элементы управления (информация и пагинация)
        language: {
            "search": "",
            searchPlaceholder: "Поиск по таблице...",
            "zeroRecords": "Ничего не найдено",
            "info": "Показаны от _START_ до _END_ из _TOTAL_ записей",
            "infoEmpty": "Показаны от 0 до 0 из 0 записей",
            "infoFiltered": "(общее кол-во записей _MAX_)",
            "lengthMenu": "_MENU_",
            "paginate": {
                "first": "Первая",
                "last": "Последняя",
                "next": "Следующая",
                "previous": "Предыдущая"
            }
        },
        buttons: [
            {
                extend: 'copy',
                className: 'custom-btn',
                titleAttr: 'Скопировать таблицу',
                message: false,
                action: function (e, dt, button, config) {
                    $.fn.dataTable.ext.buttons.copyHtml5.action.call(this, e, dt, button, config);

                    // Показать уведомление
                    $('#copyNotification').addClass('show').fadeIn(300).delay(1000).fadeOut(300, function() {
                        $(this).removeClass('show');
                    });
                }
            },
            {
                extend: 'excel',
                className: 'custom-btn',
                titleAttr: 'Скачать таблицу в формате .xlsx',
            }
            // {
            //     extend: 'pdf',
            //     className: 'custom-btn',
            //     titleAttr: 'Скачать таблицу в формате .pdf',
            // },
            // {
            //     extend: 'colvis',
            //     className: 'custom-btn',
            //     titleAttr: 'Скрыть/показать столбцы таблицы',
            //     text: 'Columns'
            // }
        ],
        responsive: true,
        lengthChange: true,
        autoWidth: true,
        paging: true,
        lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "Все"]],
        pageLength: 10,
        search: {
            caseInsensitive: true // Не учитывать регистр при поиске
        },
        columnDefs: [
            { orderable: true, targets: '_all' }
        ]
    });

    // Индивидуальный поиск по каждому столбцу
    $('#DataTable tfoot th').each(function() {
        var title = $(this).text();
        $(this).html('<input type="text" placeholder="фильтр" />');
    });

    // Применение фильтрации по каждому столбцу
    table.columns().every(function() {
        var that = this;
        $('input', this.footer()).on('keyup change', function() {
            if (that.search() !== this.value) {
                that.search(this.value, true, true).draw(); // Учитывать регистр
            }
        });
    });

});