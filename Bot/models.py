from django.db import models


class Bot_Table(models.Model):
    id = models.IntegerField(
        unique=True, primary_key=True, default=1
    )  # to be sure there's only one instance of the model
    token = models.CharField(max_length=70, null=True)
    admin_id = models.IntegerField(null=True)
    max_team_size = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if self._state.adding and self.__class__.objects.exists():
            raise T.exceptions.UniqueObjectError(
                f"There can be only one {self.__class__.__name__} instance"
            )
        super().save(*args, **kwargs)


class Key(models.Model):
    name = models.CharField(max_length=50, null=True)
    verbose_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.verbose_name


class Person(models.Model):
    id = models.IntegerField(primary_key=True)

    class Meta:
        abstract = True


class Captain(Person):
    anagraphic = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.anagraphic


class Hunter(Person):
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15, null=True)
    surname = models.CharField(max_length=50, null=True)
    age = models.IntegerField(null=True)
    uni = models.CharField(max_length=50, null=True)
    tframe = models.CharField(max_length=50, null=True)
    perc = models.IntegerField(null=True)
    captain = models.ForeignKey(
        Captain, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} {self.surname}"


class Queue(models.Model):
    situation = models.CharField(max_length=30, null=True)
    hunter = models.OneToOneField(
        Hunter, on_delete=models.CASCADE, null=True, blank=True, parent_link=True
    )

    def __str__(self):
      situation = f"{self.situation}\n"

      def cap(status):
        node_list = self.node_set.filter(status=status)
        cap_str_list = [str(node.captain) for node in node_list]
        return f"  {status}: [{', '.join(cap_str_list)}]"

      s = situation + "\n".join(map(cap, ["Accettato", "Rifiutato", "Chiesto", "Non chiesto"]))
      return s


class Node(models.Model):
    uid = models.AutoField(primary_key=True)
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, null=True, blank=True)
    captain = models.OneToOneField(
        Captain, on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.CharField(max_length=20, null=True)
    number = models.IntegerField(null=True)

    def __str__(self):
        return f"({self.captain.anagraphic}: {self.status})"
